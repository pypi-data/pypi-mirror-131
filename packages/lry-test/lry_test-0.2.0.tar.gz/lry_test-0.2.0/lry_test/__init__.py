'''
@ author of the file:garbage_classification.py:lry(Intelligent Awareness 2001)
@ garbage_classification.py 作者：刘仁宇 智能感知2001
@ all rights reserved
@ you must not use this python file in commerical use and commercial purpose
@ be careful : if you want to use this file, you must adjust the parameters by yourself
@ 注意：你应该在本文将中自己调整参数
@ garbage_classification.py version 10.0.0
@ powered by lry
@ last crerated time :2021.11.10
'''

import torch
import os
import glob
import random
import csv
from PIL import ImageTk
from PIL import Image as Im
from torchvision import transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch import nn
from matplotlib import pyplot as plt
import visdom
from torch import optim
from torchvision.models import resnet18
from torch.nn import functional as F
import codecs
import sys
import tkinter
from tkinter import *
from tkinter import messagebox
import time
import tkinter.messagebox
import webbrowser
import tkinter.filedialog
import _thread

from distutils.sysconfig import get_python_lib


root=Tk()
classes=('harmful','kitch','others','recyc')
a_loss=[]
a_accuracy=[]


'''
@ the code below is about the tools of showing the clock
@ this code was written by lry
@ the version of this function is version 1.0.0
@ time :2021.11.10
'''
def check_files():
    file000 = get_python_lib()
    a = 0
    path000 = os.path.join(file000, 'lry_test\\model.py')
    a=os.path.exists(path000)
    if a == True:
        tkinter.messagebox.showinfo('提示','所有文件都可以被找到')
    else:
        tkinter.messagebox.showerror('错误', 'model.py文件缺失，重新安装本程序可能会解决问题')

def fix_files():
    file000 = get_python_lib()
    a = 0
    path000 = os.path.join(file000, 'lry_test\\model.py')
    a = os.path.exists(path000)
    if a == True:
        tkinter.messagebox.showinfo('提示', '所有文件都可以被找到')
    else:
        tkinter.messagebox.showerror('错误', 'model.py文件缺失,并且无法被修复，也可以点击下方的按钮训练，重新安装本程序可能会解决问题')

def Test_model_old():
    file000 = get_python_lib()
    a = 0
    path000 = os.path.join(file000, 'lry_test\\model.py')
    a = os.path.exists(path000)
    b=0
    if a == True:
        tkinter.messagebox.showinfo('提示', '所有文件都可以被找到')
        b=1
    else:
        tkinter.messagebox.showerror('错误', 'model.py文件缺失,并且无法被修复，重新安装本程序可能会解决问题，或者是使用下方的训练按钮训练，点击确定以继续')
    if b==1 :
        test_model('test/1.jpg')
    else :
        print('???')
        tkinter.messagebox.showerror('无法识别','错误原因：没有模型')


def test_model(filepath):
    global root
    try:
        img=tkinter.PhotoImage(file=filepath)
        label_img=tkinter.Label(root,image=img,height=350,width=550).place(x=510,y=90)
    except:
        print('can not recognize data in image file',filepath)
        try:
            img=Im.open(filepath)
            img_png = ImageTk.PhotoImage(img)
            label_img=tkinter.Label(root,image=img_png,height=350,width=550).place(x=510,y=90)
        except:
            print('UnknownError')
            tkinter.messagebox.showerror('错误', '图片控件无法加载图片！！！')
            raise

    if torch.cuda.is_available():
        device = torch.device('cuda')
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrops(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
    else:
        device = torch.device('cpu')
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
    file000 = get_python_lib()
    a = 0
    path000 = os.path.join(file000, 'lry_test\\model.py')
    if torch.cuda.is_available():
        net = torch.load(path000, map_location='cuda')
        net = net.to(device)
        torch.no_grad()
        img = Im.open(filepath)
        img = transform(img).unsqueeze(0)
        img_ = img.to(device)
        outputs = net(img_)
        _, predicted = torch.max(outputs, 1)
    else:
        net = torch.load(path000, map_location='cpu')
        net = net.to(device)
        torch.no_grad()
        img = Im.open(filepath)
        img = transform(img).unsqueeze(0)
        img_ = img.to(device)
        outputs = net(img_)
        _, predicted = torch.max(outputs, 1)
    print(classes[predicted[0]])
    if classes[predicted[0]]=='harmful':
        tkinter.messagebox.showinfo('识别结果','有害垃圾')
    elif classes[predicted[0]]=='kitch':
        tkinter.messagebox.showinfo('识别结果','厨余垃圾')
    elif classes[predicted[0]]=='others':
        tkinter.messagebox.showinfo('识别结果','其他垃圾')
    elif classes[predicted[0]]=='recyc':
        tkinter.messagebox.showinfo('识别结果','可回收垃圾')
    else :
        tkinter.messagebox.showerror('识别结果','UNKNOWN ERROR!!!,we cannot get the result of the reconization')

def information():
    print('these information are about the copyright of this file:')
    print('\tauthor of the train.py:lry (Intelligent Awareness 2001)')
    print('\ttrain.py 作者：刘仁宇 智能感知2001')
    print('\tcopyright (c) 2020-2021')
    print('\tall rights reserved')
    print('\tyou must not use this python file in commercial use and commercial purpose')
    print('\tbe careful :if you use this file, you should adjust the parameters by yourself')
    print('\t注意：你应该在本文件中自己调整参数')
    print('\tgarbage_classification.py\tversion 1.0.0')
    tkinter.messagebox.showinfo('程序信息','these information are about the copyright of this file:\n\tauthor of the train.py:lry (Intelligent Awareness 2001)\n\ttrain.py 作者：刘仁宇 智能感知2001\n\tcopyright (c) 2020-2021\n\tall rights reserved\n\tyou must not use this python file in commercial use and commercial purpose\n\tbe careful :if you use this file, you should adjust the parameters by yourself\n\t注意：你应该在本文件中自己调整参数\n\tgarbage_classification.py\tversion 1.0.0')


class Flatten(nn.Module):
    def __init__(self):
        super(Flatten,self).__init__()
    def forward(self,x):
        shape=torch.prod(torch.tensor(x.shape[1:])).item()
        return x.view(-1,shape)
def plot_image(img,label,name):
    fig=plt.figure()
    for i in range(6):
        plt.subplot(2,3,i+1)
        plt.tight_layout()
        plt.imshow(img[i][0]*0.3081+0.1307,cmap='gray',interpolation='none')
        plt.title('{}:{}'.format(name,label[i].item()))
        plt.xticks([])
        plt.yticks([])
    plt.show()


def link_github():
    webbrowser.open('https://github.com/lry-123456789/garbage_classification')

def ask_exit():
    ans=tkinter.messagebox.askyesno('提示','确定要推出本程序吗？')
    if ans == True:
        exit(0)
    else :
        print('cancel exit the program')

def choose_file():
    print('begin to choose files')
    filepath=tkinter.filedialog.askopenfilename()
    print(filepath)
    test_model(filepath)

def thread1_open_visdom():
    time1=time.time()
    print('open_new_thread:time=>',time1)
    print('we will start a new thread,please wait')
    b=os.popen('python -m visdom.server')
    c=b.read()
    print(c)

def train():
    global root
    def evalute(model, loader):
        model.eval()
        correct = 0
        total = len(loader.dataset)
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            with torch.no_grad():
                logits = model(x)
                pred = logits.argmax(dim=1)
            correct += torch.eq(pred, y).sum().float().item()
        return correct / total
    batchsz = 64
    lr = 1e-4
    epochs = 100
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(1234)
    train_db = Data('train_data', 224, mode='train')
    val_db = Data('train_data', 224, mode='val')
    test_db = Data('train_data', 224, mode='test')
    train_loader = DataLoader(train_db, batch_size=batchsz, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_db, batch_size=batchsz, num_workers=4)
    test_loader = DataLoader(test_db, batch_size=batchsz, num_workers=4)
    viz = visdom.Visdom()
    trained_model = resnet18(pretrained=True)
    model = nn.Sequential(*list(trained_model.children())[:-1], Flatten(), nn.Linear(512, 6)).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criteon = nn.CrossEntropyLoss()
    best_acc, best_epoch = 0, 0
    global_step = 0
    viz.line([[0.0, 0.0]], [0.], win='test',
             opts=dict(title='Loss on Training Data and Accuracy on Training Data', xlabel='Epochs',
                       ylabel='Loss and Accuracy', legend=['loss', 'val_acc']))
    for epoch in range(epochs):
        for step, (x, y) in enumerate(train_loader):
            x, y = x.to(device), y.to(device)
            model.train()
            logits = model(x)
            try:
                thread1=thread1_open_visdom()
                thread1.start()
                os.open('localhost:8097')
            except:
                print('we can not start visdom')
                print('use in default mode')
                print('you may not see the graph when training')
            loss = criteon(logits, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            try:
                viz.line([[loss.item(), evalute(model, val_loader)]], [global_step], win='test', update='append')
            except:
                print('use in default mode.do not run in visualize mode')
            global_step += 1
        if epoch == 0:
            print('the ' + str(epoch + 1) + ' epoch' + ' training......')
            val_acc = evalute(model, val_loader)
            if val_acc > best_acc:
                best_epoch = epoch
                best_acc = val_acc
                torch.save(model.state_dict(), 'best_trans.mdl')
    print('best accuracy:', best_acc, 'best epoch:', (best_epoch + 1))
    file000 = get_python_lib()
    a = 0
    path000 = os.path.join(file000, 'lry_test\\model.py')
    torch.save(model, path000)
    print('loading model......')
    test_acc = evalute(model, test_loader)
    print('test accuracy:', test_acc)
    print('successfully save the best model ')

def Data_Pre():
    db = Data('train_data', 64, 'train')
    DataLoader(db, batch_size=32, shuffle=True, num_workers=8)

class Data(Dataset):
    def __init__(self,root,resize,mode):
        super(Data,self).__init__()
        self.root=root
        self.resize=resize
        self.name2label={}
        for name in sorted(os.listdir(os.path.join(root))):
            if not os.path.isdir(os.path.join(root,name)):
                continue
            self.name2label[name]=len(self.name2label.keys())
        self.images,self.labels=self.load_csv('images.csv')
        if mode=='train':
            self.images=self.images[:int(0.6*len(self.images))]
            self.labels=self.labels[:int(0.6*len(self.labels))]
        elif mode=='val':
            self.images=self.images[int(0.6*len(self.images)):int(0.8*len(self.images))]
            self.labels=self.labels[int(0.6*len(self.labels)):int(0.8*len(self.labels))]
        else:
            self.images=self.images[int(0.8*len(self.images)):]
            self.labels=self.labels[int(0.8*len(self.images)):]
    def load_csv(self,filename):
        if not os.path.exists(os.path.join(self.root,filename)):
            images=[]
            for name in self.name2label.keys():
                images+=glob.glob(os.path.join(self.root,name,'*.png'))
                images+=glob.glob(os.path.join(self.root,name,'*.jpg'))
                images+=glob.glob(os.path.join(self.root,name,'*.jpeg'))
            print(len(images))
            random.shuffle(images)
            with open(os.path.join(self.root,filename),mode='w',nemline='') as f:
                writer=csv.writer(f)
                for img in images:
                    name=img.split(os.sep)[-2]
                    label=self.name2label[name]
                    writer.writerow([img,label])
                print('write into csv into :',filename)
        images,labels=[],[]
        with open(os.path.join(self.root,filename)) as f:
            reader=csv.reader(f)
            for row in reader:
                img,label=row
                label=int(label)
                images.append(img)
                labels.append(label)
        assert len(images)==len(labels)
        return images,labels
    def __len__(self):
        return len(self.images)
    def denormalize(self,x_hat):
        mean=[0.485,0.456,0.406]
        std=[0.229,0.224,0.225]
        mean=torch.tensor(mean).unsqueeze(1).unsqueeze(1)
        std=torch.tensor(std).unsqueeze(1).unsqueeze(1)
        x=x_hat*std+mean
        return x
    def __getitem__(self,idx):
        img,label=self.images[idx],self.labels[idx]
        tf=transforms.Compose([lambda x:Image.open(x).convert('RGB'),transforms.Resize((int(self.resize*1.25),int(self.resize*1.25))),transforms.RandomRotation(15),transforms.CenterCrop(self.resize),transforms.ToTensor(),transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])])
        img=tf(img)
        label=torch.tensor(label)
        return img,label

file000 = get_python_lib()
a = 0
path000=os.path.join(file000,'lry_test\\model.py')
root.title('垃圾分类程序 version 10.0.0')
root.geometry('1077x640')
a_file=os.path.exists('path000')
if a==0:
    if a_file == True:
        a=a+1
    else:
        try:
            #os.rename('C:\\model_lry\\model.py','C:\\model_lry\\model.py')
            a=a+1
        except:
            #tkinter.messagebox.showerror('错误', 'C:\\model_lry\\model.py文件缺失，重新安装本程序可能会解决问题')
            a=a+1
b1=Button(root,text='文件检查',height=3,width=18,command=check_files).place(x=100,y=20)
b2=Button(root,text='文件缺失修复',height=3,width=18,command=fix_files).place(x=250,y=20)
b3=Button(root,text='启动主程序并进行自动分类操作\n(默认路径.test1.jpg)',height=3,width=40,command=Test_model_old).place(x=100,y=100)
b4=Button(root,text='本程序信息',height=3,width=18,command=information).place(x=100,y=180)
b5=Button(root,text='源代码(github)',height=3,width=18,command=link_github).place(x=250,y=180)
b6=Button(root,text='退出',height=3,width=40,command=ask_exit).place(x=100,y=260)
b7=Button(root,text='选择文件并识别',height=1,width=20,command=choose_file).place(x=900,y=30)
b8=Button(root,text='训练模型并且启动可视化工具',height=3,width=40,command=train).place(x=100,y=340)
'''
l1=Label(root,text='图片分析处理进度',height=1,width=14).place(x=10,y=330)
l2=Label(root,text='必要文件检查进度',height=1,width=14).place(x=10,y=360)
l3=Label(root,text='python环境检查进度',height=1,width=16).place(x=10,y=390)
l4=Label(root,text='0%',height=1,width=20).place(x=130,y=330)
l5=Label(root,text='0%',height=1,width=20).place(x=130,y=360)
l6=Label(root,text='0%',height=1,width=20).place(x=130,y=390)
'''
l7=Label(root,text='详细信息:',height=1,width=20).place(x=10,y=420)
l8=Label(root,text='文件路径:',height=1,width=20).place(x=450,y=35)
t1=Text(root,height=10,width=146).place(x=30,y=450)
t2=Text(root,height=2,width=45).place(x=560,y=30)
t3=Text(root,height=25,width=77).place(x=510,y=90)
root.mainloop()
