import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def cv_show_image(title, image, type='rgb'):
    channels=image.shape[-1]
    if channels==3 and type=='rgb':
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 将BGR转为RGB
    cv2.imshow(title, image)
    cv2.waitKey(0)

def get_prewhiten_image(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1 / std_adj)
    return y

def image_normalization(image,mean=None,std=None):
    image = np.array(image, dtype=np.float32)
    image = image / 255.0
    if mean is not None:
        image=np.subtract(image, mean)
    if std is not None:
        np.multiply(image, 1 / std)
    return image

def get_prewhiten_images(images_list,normalization=False):
    out_images=[]
    for image in images_list:
        if normalization:
            image=image_normalization(image)
        image=get_prewhiten_image(image)
        out_images.append(image)
    return out_images

def read_image_gbk(filename, resize_height=None, resize_width=None, normalization=False,colorSpace='RGB'):
    with open(filename, 'rb') as f:
        data = f.read()
        data = np.asarray(bytearray(data), dtype="uint8")
        bgr_image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if bgr_image is None:
        print("Warning:不存在:{}", filename)
        return None
    if len(bgr_image.shape) == 2:  # 若是灰度图则转为三通道
        print("Warning:gray image", filename)
        bgr_image = cv2.cvtColor(bgr_image, cv2.COLOR_GRAY2BGR)
    if colorSpace=='RGB':
        image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)  # 将BGR转为RGB
    elif colorSpace=="BGR":
        image=bgr_image
    else:
        exit(0)
    image = resize_image(image,resize_height,resize_width)
    image = np.asanyarray(image)
    if normalization:
        image=image_normalization(image)
    return image

def resize_image(image,resize_height, resize_width):
    image_shape=np.shape(image)
    height=image_shape[0]
    width=image_shape[1]
    if (resize_height is None) and (resize_width is None):#错误写法：resize_height and resize_width is None
        return image
    if resize_height is None:
        resize_height=int(height*resize_width/width)
    elif resize_width is None:
        resize_width=int(width*resize_height/height)
    image = cv2.resize(image, dsize=(resize_width, resize_height))
    return image

def get_rect_image(image,rect):
    shape=image.shape#h,w
    height=shape[0]
    width=shape[1]
    image_rect=(0,0,width,height)
    rect=get_rect_intersection(rect, image_rect)
    x, y, w, h=rect
    cut_img = image[y:(y+ h),x:(x+w)]
    return cut_img


def get_rects_image(image,rects_list,resize_height=None, resize_width=None):
    rect_images = []
    for rect in rects_list:
        roi=get_rect_image(image, rect)
        roi=resize_image(roi, resize_height, resize_width)
        rect_images.append(roi)
    return rect_images

def get_bboxes_image(image,bboxes_list,resize_height=None, resize_width=None):
    rects_list=bboxes2rects(bboxes_list)
    rect_images = get_rects_image(image,rects_list,resize_height, resize_width)
    return rect_images

def bboxes2rects(bboxes_list):
    rects_list=[]
    for bbox in bboxes_list:
        x1, y1, x2, y2=bbox
        rect=[ x1, y1,(x2-x1),(y2-y1)]
        rects_list.append(rect)
    return rects_list

def rects2bboxes(rects_list):
    bboxes_list=[]
    for rect in rects_list:
        x1, y1, w, h = rect
        x2=x1+w
        y2=y1+h
        b=(x1,y1,x2,y2)
        bboxes_list.append(b)
    return bboxes_list

def get_rect_intersection(rec1,rec2):
    cx1, cy1, cx2, cy2 = rects2bboxes([rec1])[0]
    gx1, gy1, gx2, gy2 = rects2bboxes([rec2])[0]
    x1 = max(cx1, gx1)
    y1 = max(cy1, gy1)
    x2 = min(cx2, gx2)
    y2 = min(cy2, gy2)
    w = max(0, x2 - x1)
    h = max(0, y2 - y1)
    return (x1,y1,w,h)

def show_image_bboxes_text(title, rgb_image, boxes, boxes_name):
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    for name ,box in zip(boxes_name,boxes):
        box=[int(b) for b in box]
        cv2.rectangle(bgr_image, (box[0],box[1]),(box[2],box[3]), (0, 255, 0), 2, 8, 0)
        cv2.putText(bgr_image,name, (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    cv_show_image(title, rgb_image)

def get_image_bboxes_text_han(img, boxes, boxes_name):
    for name, box in zip(boxes_name, boxes):
        box = [int(b) for b in box]
        cv2.rectangle(img, (box[0],box[1]),(box[2],box[3]), (0, 255, 0), 2, 8, 0)

    cv2_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_img)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype('simhei.ttf', 20, encoding='utf-8')
    for name, box in zip(boxes_name, boxes):
        box = [int(b) for b in box]
        draw.text((box[0], box[1]), name,fill='blue',font=font)
    rgb_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
    return rgb_img


def save_image(image_path, rgb_image,toUINT8=True):
    if toUINT8:
        rgb_image = np.asanyarray(rgb_image * 255, dtype=np.uint8)
    if len(rgb_image.shape) == 2:  # 若是灰度图则转为三通道
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_GRAY2BGR)
    else:
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(image_path, bgr_image)

def scaled_to(x, y, w, h):
    # 对x*y的图像与w*h的边框做适配
    if x / y > w / h:
        x, y = w, round(y * w / x)
    else:
        x, y = round(x * h / y), h
    return x, y

if __name__=="__main__":
    print(scaled_to(10, 6, 20, 20))
