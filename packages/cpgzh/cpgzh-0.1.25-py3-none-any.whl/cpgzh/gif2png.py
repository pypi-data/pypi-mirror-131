import os
from PIL import Image,ImageSequence

def gif2png(image):
    '将gif动画拆解成每一帧png的函数'
    image_dir=os.path.dirname(image)
    head,name=os.path.split(image)
    name=name[:-4]
    image_dir=os.path.join(image_dir,name)
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir)
    img=Image.open(image)
    # 创建读取每一帧的迭代器
    iter = ImageSequence.Iterator(img)
    index=1
    images=[]
    for i in iter:
        now_img=os.path.join(image_dir,f"{name}({index}).png")
        i.save(now_img)
        images.append(now_img)
        index+=1
    return images