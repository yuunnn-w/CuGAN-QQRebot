import requests
import json
from ctypes import *
import os.path as osp
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch
import os
from skimage import io
import threading
import time
from CUGAN import CuGAN#导入CUGAN模型处理文件
class Cell :#匹配模板细胞，细胞组成了整个回复模板库
    def __init__(self,input,output,key,next):
        self.input = input#输入模板
        self.output = output#回复
        self.key = key#输入模板中的关键词，检测到关键词会加分
        self.next = next#额外输出的话，用于补充输出
class Data :#回复模板库类
    def __init__(self):
        self.dll = CDLL('./test.dll')#加载C语言编写的dll动态库
        self.list1 = list()
        self.list2 = list()
        self.list3 = list()
        self.list4 = list()
        self.list0 = list()
    def list_1(self,input,output,key,next):
        cell = Cell(input,output,key,next)
        self.list1.append(cell)
    def list_2(self,input,output,key,next):
        cell = Cell(input,output,key,next)
        self.list2.append(cell)
    def list_3(self,input,output,key,next):
        cell = Cell(input,output,key,next)
        self.list3.append(cell)
    def list_4(self,input,output,key,next):
        cell = Cell(input,output,key,next)
        self.list4.append(cell)
    def list_0(self,input,output,key,next):
        cell = Cell(input,output,key,next)
        self.list0.append(cell)
    def initilization(self,file_path='word.txt'):#初始化方法，从word.txt数据库中加载模板
        word = list()
        with open(file_path, encoding='utf-8') as file_obj:
            for line in file_obj:
                if line.replace('\n','') == '':
                    continue
                else :
                    word.append(line.replace('\n',''))
        i=0
        while(1):
            if word[i]=='吃有关的对话':#加载不同的回复类型
                i+=1
                while(1):
                    i+=4
                    c=word[i-4:i]
                    if c[0]=='0' and c[1]=='0' :
                        i-=4
                        break
                    self.list_1(c[0],c[1],c[2],c[3])
            if word[i]=='玩有关的对话':
                i+=1
                while(1):
                    i+=4
                    c=word[i-4:i]
                    if c[0]=='0' and c[1]=='0' :
                        i-=4
                        break
                    self.list_2(c[0],c[1],c[2],c[3])
            if word[i]=='爱有关的对话':
                i+=1
                while(1):
                    i+=4
                    c=word[i-4:i]
                    if c[0]=='0' and c[1]=='0' :
                        i-=4
                        break
                    self.list_3(c[0],c[1],c[2],c[3])
            if word[i]=='安慰有关的对话':
                i+=1
                while(1):
                    i+=4
                    c=word[i-4:i]
                    if c[0]=='0' and c[1]=='0' :
                        i-=4
                        break
                    self.list_4(c[0],c[1],c[2],c[3])
            if word[i]=='其他有关的对话':
                i+=1
                while(1):
                    i+=4
                    c=word[i-4:i]
                    if c[0]=='0' and c[1]=='0' :
                        i-=4
                        break
                    self.list_0(c[0],c[1],c[2],c[3])
            i+=1
            if word[i]=='end':
                break;
        self.list0+=self.list1
        self.list0+=self.list2
        self.list0+=self.list3
        self.list0+=self.list4
    def match_all(self,input_sentence):#在所有模板中进行混合匹配
        index=0#选择的回复细胞索引
        max1=-999#相似度分数
        for i in range(len(self.list0)):
            s = self.dll.Matching(input_sentence,self.list0[i].input,self.list0[i].key)#得到输入句子和模板的相似度分数
            if s > max1 :#如果遍历的细胞得分大于之前的最高分
                index = i#更新索引
                max1 = s#更新最高分
            else :
                continue
        return self.list0[index].output+'\n'+self.list0[index].next.replace('0','')#返回模板细胞中的回复和next补充回复
    def match_key(self,input_sentence):#首先进行关键词匹配
        output_sentence=''
        if input_sentence.find('吃') != -1 :#如果检测到吃这个关键词，就到对应的关键词模板库进行优先匹配
            index=0
            max1=-999
            for i in range(len(self.list1)):
                s = self.dll.Matching(input_sentence,self.list1[i].input,self.list1[i].key)
                if s > max1 :
                    index = i
                    max1 = s
                else :
                    continue
            if s < 3 :
                output_sentence = self.match_all(input_sentence)#如果得分小于三分，就进行总体混合匹配
            else :
                output_sentence = self.list1[index].output+'\n'+self.list1[index].next.replace('0','')
            return output_sentence
        if input_sentence.find('玩') != -1 :
            index=0
            max1=-999
            for i in range(len(self.list2)):
                s = self.dll.Matching(input_sentence,self.list2[i].input,self.list2[i].key)
                if s > max1 :
                    index = i
                    max1 = s
                else :
                    continue
            if s < 3 :
                output_sentence = self.match_all(input_sentence)
            else :
                output_sentence = self.list2[index].output+'\n'+self.list2[index].next.replace('0','')
            return output_sentence
        if input_sentence.find('爱') != -1 :
            index=0
            max1=-999
            for i in range(len(self.list3)):
                s = self.dll.Matching(input_sentence,self.list3[i].input,self.list3[i].key)
                if s > max1 :
                    index = i
                    max1 = s
                else :
                    continue
            if s < 3 :
                output_sentence = self.match_all(input_sentence)
            else :
                output_sentence = self.list3[index].output+'\n'+self.list3[index].next.replace('0','')
            return output_sentence
        if input_sentence.find('死') != -1 :
            index=0
            max1=-999
            for i in range(len(self.list4)):
                s = self.dll.Matching(input_sentence,self.list4[i].input,self.list4[i].key)
                if s > max1 :
                    index = i
                    max1 = s
                else :
                    continue
            if s < 3 :
                output_sentence = self.match_all(input_sentence)
            else :
                output_sentence = self.list4[index].output+'\n'+self.list4[index].next.replace('0','')
            return output_sentence
        output_sentence = self.match_all(input_sentence)
        return output_sentence
data = Data()#初始化数据库类
data.initilization('word.txt')#加载数据库
class SendPic(threading.Thread):#发送图片线程类，继承自threading.Thread
    def __init__(self,url,gid):
        threading.Thread.__init__(self)
        self.url=url#输入参数为url和gid群号
        self.gid=gid
    def run(self):
        URL = None#图床返回的图片URL
        gid = self.gid
        url = self.url#QQ传来的url
        path = CuGAN(url,'up3x-latest-conservative.pth')#调用超分函数，得到超分后的图片保存路径
        headers = {'Authorization': 'DD6zfzpIaxwgcBk3Zht0hPZ4hm0H8u*G'}#请求头要包含SM.MS图床给出的密钥，需要自己注册获取
        files = {'smfile': open(path, 'rb')}#打开文件
        url = 'https://sm.ms/api/v2/upload'#上传的地址
        res = requests.post(url, files=files, headers=headers).json()#获得服务器返回的json
        print(res)
        if res['success'] == False:#如果上传失败，说明图片已存在
            URL = res['images']
        else :
            URL = res['data']['url']#上传成功，获得图床中的图片url
        put = 'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}&auto_escape=false'#返回给酷Q前端的地址
        pic_path = r'[CQ:image,' r'file=' + URL + r']'#图片CQ码
        requests.get(url=put.format(gid, pic_path))#
T1=None#全局变量，记录调用超分辨率函数的时间差，只允许五秒调用一次，防止硬件过载
T2=None
def keyword(message, uid, gid=None):#处理前端传来的信息
    global T1#声明全局变量
    global T2
    print(message)
    index=message.find("[CQ:at,qq=3376166185]")#如果是艾特自己的消息，这里是我的小号的QQ号
    indexurl=message.find("url=https://")#如果找到的url信息
    ESRGAN = message.find("超分辨率")#如果找到了超分辨率这几个字
    if index != -1 :
        index2 = message.find("]")#获取信息的结尾
        if gid:#如果是群聊消息
            put = 'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}&auto_escape=false'
            requests.get(url=put.format(gid,data.match_key(message[index2+2:])))#自动匹配词典进行回复
            #print(message[index2+2:])
        else :#私聊回复
            put = 'http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}&auto_escape=false'
            requests.get(url=put.format(uid,data.match_key(message[index2+2:])))#这个私聊回复的功能暂时起不了作用，可以自己修改一下
    if ESRGAN != -1:#如果找到了超分辨率这四个字
        if T1 !=None :
            T2=time.time()#计时
            T = T2-T1
            if T<=5 :#如果两次调用间隔小于五秒
                if gid :
                     put = 'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}&auto_escape=false'
                     requests.get(url=put.format(gid, '稍等一下，超分功能正在冷却中'))#提示
                return
        indexurl=message.find("url=https://")#获取图片URL

        if indexurl != -1 :#如果找到了url
            url = message[indexurl+4:]
            end = url.find("]")#获取结尾
            url = url[:end]#获取整个url
            #print(url)
            if gid:
                 Send_Pic = SendPic(url,gid)#建立发图片线程，这里采用线程异步处理，防止服务器堵塞
                 Send_Pic.start()#线程开始
                 T1 = time.time()#结束计时

def setu(uid, gid=None):#涩图功能，未启用
    num = 1
    url = 'https://api.lolicon.app/setu'
    params = {'r18': 0,
              'size1200': True,
              'num': num}
    menu = requests.get(url, params=params)
    # print(menu.json()['data'][0]['urls']['original'])
    for i in range(num):
        print(menu.json()['data'][i]['url'])
        setu_url = menu.json()['data'][i]['url'] 
        if gid:
            put = 'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}&auto_escape=false'
            pic_path = r'[CQ:image,' r'file=' + setu_url + r']'
            print(pic_path)
            requests.get(url=put.format(gid, pic_path))
            requests.get(url=put.format(gid, '已经发了一张图，没看到就是被吞了'))
        else:
            print(uid)
            put = 'http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}&auto_escape=false'
            pic_path = r'[CQ:image,' r'file=' + setu_url + r']'
            print(pic_path)
            requests.get(url=put.format(uid, pic_path))