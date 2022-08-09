import urllib.request as urllib2
from PIL import Image
from io import BytesIO 
from io import StringIO
import requests
import uuid
import os
import torch
import cv2
from upcunet_v3 import RealWaifuUpScaler
from time import time as ttime
def CuGAN(url,ModelName):#输入QQ中的URL和处理模型的名字
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}#请求头加上用户头不然不会被服务器响应
    req=requests.get(url,headers=headers)
    image=Image.open(BytesIO(req.content))#将图片下载到本地
    #print(image.shape)
    fileName=str(uuid.uuid4())+'.'+image.format.lower()#获取文件名以及文件类型
    os.makedirs('pic/',exist_ok=True)#创建pic文件夹
    with open('pic/'+fileName,'wb') as f:#保存图片文件
        f.write(req.content)
    path = 'pic/'+fileName#图片读取路径
    t0 = ttime()#计时
    ModelPath="model/"#模型路径
    upscaler = RealWaifuUpScaler(3, ModelPath+ModelName, half=True, device="cuda:0")#第一个参数是放大倍数，需要根据选择的模型进行修改，3意味着选择x3模型
    #使用CPU可修改参数为device='cpu'
    torch.cuda.empty_cache()
    try:
        img = cv2.imread(path)[:, :, [2, 1, 0]]
        #print(img.shape)
        result = upscaler(img,tile_mode=5,cache_mode=2,alpha=1)
        #print(result.shape)
        os.remove(path)#删除源文件
        path=path.split('.')[0]+'.jpg'#将文件保存为jpg有损压缩格式节省空间
        cv2.imwrite(path,result[:, :, ::-1])
    except RuntimeError as e:#抛出异常
        print (path+" FAILED")
        print (e)
    else:
        print(path+" DONE")
        #os.remove(PendingPath+i)
    t1 = ttime()
    print("time_spent", t1 - t0)#打印Forward时间
    return path