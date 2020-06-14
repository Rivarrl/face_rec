# -*- coding: utf-8 -*-
# ======================================
# @File    : dataset_creator.py
# @Time    : 2020/6/10 1:03
# @Author  : Rivarrl
# ======================================
import numpy as np
from utils import image_processing , file_processing
import face_rec
import os
import shutil

resize_width = 160
resize_height = 160

def osjoin(*args):
    return os.sep.join(args)

def classify_faces(dataset_path):
    # 将人脸图像分为0，1和n>1张脸三类，存到三个文件夹下，供后续人工简单筛选用
    face_detect = face_rec.FaceDetection()
    classify_root_path = './data/classify'
    classify_path = [osjoin(classify_root_path, x) for x in ('NA', '0', '1', 'n')]
    for tp in classify_path:
        if os.path.exists(tp): continue
        os.mkdir(tp)
    paths = os.listdir(dataset_path)
    for img_path in paths:
        real_path = osjoin(dataset_path, img_path)
        image = image_processing.read_image_gbk(real_path, colorSpace='RGB')
        if not isinstance(image, np.ndarray):
            out_put_path = osjoin(classify_path[0], img_path)
        else:
            bboxes, landmarks = face_detect.detect_face(image)
            bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks,fixed="height")
            if bboxes == [] or landmarks == []:
                out_put_path = osjoin(classify_path[1], img_path)
            elif len(bboxes) >= 2 or len(landmarks) >= 2:
                out_put_path = osjoin(classify_path[3], img_path)
            else:
                out_put_path = osjoin(classify_path[2], img_path)
        shutil.copy(real_path, out_put_path)

def get_face_embedding(model_path,files_list, names_list):
    # 获得embedding数据
    colorSpace="RGB"
    face_detect = face_rec.FaceDetection()
    face_net = face_rec.FacenetEmbedding(model_path)

    embeddings=[]
    label_list=[]
    for image_path, name in zip(files_list, names_list):
        print("processing image :{}".format(image_path))
        image = image_processing.read_image_gbk(image_path, colorSpace=colorSpace)
        if not isinstance(image, np.ndarray): continue
        bboxes, landmarks = face_detect.detect_face(image)
        bboxes, landmarks =face_detect.get_square_bboxes(bboxes, landmarks,fixed="height")
        if bboxes == [] or landmarks == []:
            print("-----no face")
            continue
        if len(bboxes) >= 2 or len(landmarks) >= 2:
            print("-----image have {} faces".format(len(bboxes)))
            continue
        face_images = image_processing.get_bboxes_image(image, bboxes, resize_height, resize_width)
        face_images = image_processing.get_prewhiten_images(face_images,normalization=True)
        pred_emb = face_net.get_embedding(face_images)
        embeddings.append(pred_emb)
        label_list.append(name)
    return embeddings,label_list

def create_face_embedding(model_path,dataset_path,out_emb_path,out_filename):
    # 建立npy文件
    files_list,names_list=file_processing.gen_files_labels(dataset_path,postfix=['*.jpg'])
    embeddings,label_list=get_face_embedding(model_path,files_list, names_list)
    print("label_list:{}".format(label_list))
    print("have {} label".format(len(label_list)))
    embeddings=np.asarray(embeddings)
    np.save(out_emb_path, embeddings)
    file_processing.write_list_data(out_filename, label_list, mode='w')

if __name__ == '__main__':
    dataset_path = './data/raw_data/perform'
    model_path = './data/model/20200208-232914'
    out_emb_path = './data/dataset/perform/data.npy'
    out_filename = './data/dataset/perform/name.txt'
    # classify_faces(dataset_path)
    create_face_embedding(model_path, dataset_path, out_emb_path, out_filename)
