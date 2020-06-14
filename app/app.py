# -*- coding: utf-8 -*-
# ======================================
# @File    : app.py
# @Time    : 2020/5/30 10:59
# @Author  : Rivarrl
# ======================================
import sys
import time

from PyQt5.Qt import Qt as PyQt5Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from main_window import Ui_MainWindow
from picture_rec import Ui_Dialog as Pic_Ui_Dialog
from camera_rec import Ui_Dialog as Cam_Ui_Dialog
from register import Ui_Dialog as Reg_Ui_Dialog
from video_rec import Ui_Dialog as Video_Ui_Dialog
from settings import Ui_Dialog as Settings_Ui_Dialog
import face_rec
from utils import file_processing, image_processing
import shutil
import cv2
import os
import cgitb
import threading

cgitb.enable()

def osjoin(*args):
    return os.sep.join(args)

root_path = os.path.abspath(os.path.join(os.getcwd(), "."))
face_detect, face_net, dataset_embedding, name_list = [None] * 4
resize_height = resize_width = 160
default_height, default_width = 480, 640
cache_path = osjoin(root_path, 'data', 'cache')
dataset_root_path = osjoin(root_path, 'data', 'dataset')
model_root_path = osjoin(root_path, 'data', 'model')
dataset_name = 'data.npy'
nameset_name = 'name.txt'

def image_fix(image):
    # 处理图像,主逻辑
    bboxes, landmarks = face_detect.detect_face(image)
    bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks, fixed='height')
    if bboxes and landmarks:
        face_images = image_processing.get_bboxes_image(image, bboxes, resize_height, resize_width)
        face_images = image_processing.get_prewhiten_images(face_images)
        pred_emb = face_net.get_embedding(face_images)
        pred_name, pred_score = file_processing.compare_embedding(pred_emb, dataset_embedding, name_list)
        show_info = [n + ':' + str(s)[:5] for n, s in zip(pred_name, pred_score)]
        image = image_processing.get_image_bboxes_text_han(image, bboxes, show_info)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

class PicDialog(QDialog, Pic_Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.resize_width = 160
        self.resize_height = 160

        self.push_button_selectpic.clicked.connect(self.select_image)
        self.pushButton.clicked.connect(self.about)
        self.pushButton_2.clicked.connect(self.close)

    def about(self):
        reply = QMessageBox.about(self,
                                  "说明",
                                  "图像识别模块")

    def select_image(self):
        img_name, img_type = QFileDialog.getOpenFileName(self,
                                                         "打开图片",
                                                         "./data/test",
                                                         "*.jpg;;*.png;;All Files(*)")
        if not img_name: return
        fixed_img = osjoin(cache_path, img_name.split('/')[-1])
        shutil.copy(img_name, fixed_img)
        image = image_processing.read_image_gbk(fixed_img)
        image = image_fix(image)
        cv2.imwrite(fixed_img, image)
        iw, ih = image.shape[1], image.shape[0]
        rw, rh = self.rec_result.width(), self.rec_result.height()
        w, h = image_processing.scaled_to(iw, ih, rw, rh)
        img = QtGui.QPixmap(fixed_img).scaled(w, h)
        self.rec_result.setAlignment(Qt.AlignCenter)
        self.rec_result.setPixmap(img)
        os.remove(fixed_img)


class CamDialog(QDialog, Cam_Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.cap = cv2.VideoCapture()
        self.timer_camera = QTimer()
        self.CAM_NUM = 0

        self.pushButton.clicked.connect(self.about)
        self.pushButton_2.clicked.connect(self.close)
        self.push_button_cam.clicked.connect(self.camera_click)
        self.timer_camera.timeout.connect(self.show_camera)

    def camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QMessageBox.warning(self, "Warning", "请检测相机与电脑是否连接正确",
                                          buttons=QMessageBox.Ok,
                                          defaultButton=QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.push_button_cam.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label.clear()
            self.push_button_cam.setText(u'打开相机')

    def show_camera(self):
        flag, self.image = self.cap.read()
        img = cv2.resize(self.image, (default_width, default_height))
        show = image_fix(img)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def about(self):
        reply = QMessageBox.about(self,
                                  "说明",
                                  "摄像机识别模块")

    def closeEvent(self, event):
        msg = QMessageBox.information(self,
                                      '关闭',
                                      '确认关闭？',
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()
        else:
            event.ignore()

class VideoDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.push_button_selectvideo = QPushButton()
        self.label_title = QLabel()
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_title.setFont(font)
        self.pushButton = QPushButton()
        self.pushButton_2 = QPushButton()

        self.label_title.setText("视频识别")
        self.push_button_selectvideo.setText("选择视频")
        self.pushButton.setText("说明")
        self.pushButton_2.setText("返回")

        self.push_button_selectvideo.clicked.connect(self.open_video)
        self.cap = cv2.VideoCapture()
        self.pushButton.clicked.connect(self.about)
        self.pushButton_2.clicked.connect(self.close)
        self.rec_result = QLabel()
        self.rec_result.setText('')

        menu = QHBoxLayout()
        menu.setContentsMargins(0, 0, 0, 0)
        menu.addWidget(self.push_button_selectvideo)
        menu.addWidget(self.pushButton)
        menu.addWidget(self.pushButton_2)

        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.rec_result)
        layout.addLayout(menu)
        self.setLayout(layout)

    def about(self):
        reply = QMessageBox.about(self,
                                  "说明",
                                  "视频识别模块")

    def open_video(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                               '选择视频文件',
                                               "./data/test",
                                               "*.mp4;;*.avi;;All Files(*)")
        if not filename: return
        self.cap = cv2.VideoCapture(filename)
        th = threading.Thread(target=self.show_video)
        th.start()

    def show_video(self):
        success, img = self.cap.read()
        while success:
            height, width = img.shape[:2]
            show = image_fix(img)
            show = QtGui.QImage(show, width, height, QtGui.QImage.Format_RGB888)
            self.rec_result.setPixmap(QtGui.QPixmap.fromImage(show))
            success, img = self.cap.read()
            time.sleep(0.2)

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
            self.rec_result.setText('')
        event.accept()

class SettingsDialog(QDialog, Settings_Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.confirm_cache = set()
        self.line_edit_path.setPlaceholderText('点击选择数据库根目录路径')
        self.line_edit_path_2.setPlaceholderText('点击选择模型根目录路径')
        self.line_edit_path.setEnabled(False)
        self.line_edit_path_2.setEnabled(False)
        self.push_button_selectpath.clicked.connect(self.select_dataset_dir)
        self.push_button_selectpath_2.clicked.connect(self.select_model_dir)
        self.checkBox.stateChanged.connect(self.confirm)
        self.change_combobox_item(self.comboBox, self.line_edit_path, dataset_root_path)
        self.change_combobox_item(self.comboBox_2, self.line_edit_path_2, model_root_path)
        self.checkBox.setChecked(True)

    def confirm(self, state):
        if state == Qt.Checked:
            default_dataset_dir = osjoin(dataset_root_path, self.comboBox.currentText())
            dataset_path = osjoin(default_dataset_dir, dataset_name)
            filename = osjoin(default_dataset_dir, nameset_name)
            model_path = osjoin(model_root_path, self.comboBox_2.currentText())
            _confirm_cache = {default_dataset_dir, dataset_path, filename, model_path}
            if self.confirm_cache != _confirm_cache:
                self.confirm_cache = _confirm_cache
                global face_net, face_detect, dataset_embedding, name_list
                dataset_embedding, name_list = file_processing.load_dataset(dataset_path, filename)
                face_detect = face_rec.FaceDetection()
                face_net = face_rec.FacenetEmbedding(model_path)
            self.push_button_selectpath.setEnabled(False)
            self.push_button_selectpath_2.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.comboBox_2.setEnabled(False)
        else:
            self.push_button_selectpath.setEnabled(True)
            self.push_button_selectpath_2.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(True)

    def change_combobox_item(self, combobox, line_edit_path, path):
        line_edit_path.setText(path)
        arr = [e for e in os.listdir(path) if os.path.isdir(os.path.join(path, e))]
        combobox.clear()
        for e in arr:
            combobox.addItem(e)

    def select_dataset_dir(self):
        global dataset_root_path
        _root_path = QFileDialog.getExistingDirectory(self,
                                                        "选择数据库根目录",
                                                        "")
        if not _root_path: return
        dataset_root_path = _root_path
        self.change_combobox_item(self.comboBox, self.line_edit_path, dataset_root_path)

    def select_model_dir(self):
        global model_root_path
        _root_path = QFileDialog.getExistingDirectory(self,
                                                      "选择模型文件夹根目录",
                                                      "")
        if not _root_path: return
        model_root_path = _root_path
        self.change_combobox_item(self.comboBox_2, self.line_edit_path_2, model_root_path)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pic_dialog = PicDialog()
        self.cam_dialog = CamDialog()
        self.video_dialog = VideoDialog()
        self.settings_dialog = SettingsDialog()
        self.push_button_about.clicked.connect(self.show_about)
        self.push_button_exit.clicked.connect(self.close)
        self.push_button_camera.clicked.connect(self.camera_window)
        self.push_button_picture.clicked.connect(self.picture_window)
        self.push_button_video.clicked.connect(self.video_window)
        self.push_button_settings.clicked.connect(self.settings_window)

    def show_about(self):
        reply = QMessageBox.about(self,
                                  "关于",
                                  "人脸识别系统v1.0")

    def show_dataset_warning(self):
        reply = QMessageBox.warning(self,
                                    "提示",
                                    "请先在设置中勾选确定后再使用识别功能")

    def settings_window(self):
        self.settings_dialog.show()

    def camera_window(self):
        self.cam_dialog.show()

    def video_window(self):
        self.video_dialog.show()

    def picture_window(self):
        self.pic_dialog.show()

if __name__ == '__main__':
    # 高分辨率自适应
    QCoreApplication.setAttribute(PyQt5Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
