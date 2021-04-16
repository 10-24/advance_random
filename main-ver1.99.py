import random
import csv
import json
import time
import sys
import threading
import tkinter as tk
from tkinter import messagebox 
import webbrowser as web

def add():
	global n
	if theLB.get(0) in lucky_dogs:
		n=h.get(theLB.get(0))
		n=int(n)
		n=n+1
		h[theLB.get(0)]=n
	else:
		pass

def add_super_no():
	global superlucky
	superlucky=list(set(names)-set(lucky_dogs)-set(nolucky))


#重置nolucky
def rest_nolucky():
	
	with open ("nolucky.json","r+")as write_file:
		write_file.truncate()
		print("清空nolucky.json成功")
	load_nolucky()
	nolucky=list(names)
	print("加载普通池子和up池子成功")

#加载superlucky和nolucky
def load_nolucky():
	global nolucky
	try:
		with open ("nolucky.json","r") as read_file:
			nolucky=json.load(read_file)
			print("载入nolucky.json成功")
			add_super_no()
	except:
		superlucky=[]
		nolucky=list(names)
		print("未发现nolucky.json")


def a_or_b():
	i=random.randint(1,4)
	return i



#show的实际调用代码
def show_dog(l):
	random.shuffle(l)
	try:
		return l[0]
	except:
		pass

#choice的实际调用代码
#l=传入列表
#
#名字显示到框框
#
#h={名字，次数}
#n=次数
#排序
def choice_noluckydog(l):
	global dog
	random.shuffle(l)
	dog=l[0]
	lucky_dogs.append(dog)
	l.remove(dog)
	theLB.insert("0",dog)
	add()
	pai()
	bai()
	print(theLB.get(0),n)
	print("from up池子")

def choice_alreadydog(l):
	global dog
	if len(l)==0:
		choice_noluckydog(nolucky)
	else:
		random.shuffle(l)
		dog=l[0]
		lucky_dogs.append(dog)
		theLB.insert("0",dog)
		add()
		pai()
		bai()
		print(theLB.get(0),n)
		print("from 普通池子")
		

#加载人名,ID,json和配置文件
def load():
	global h
	global db
	global bd
	global ren
	global sec
	global size
	configname="configuration.csv"
	with open (configname) as f:
		reader=csv.reader(f)
		header_row=next(reader)
		global names
		global ID
		names=[]
		id=[]
		lren=[]
		lsec=[]
		sizes=[]
		for row in reader:
			names.append(row[0])
			id.append(row[1])
			lren.append(row[2])
			lsec.append(row[3])
			sizes.append(row[4])
		db=dict(zip(names,id))
		bd=dict(zip(id,names))
		ren=lren[0]
		sec=lsec[0]
		size=sizes[0]
		print("初始化配置成功")
	try:
		with open("times.json","r") as read_file:
			h=json.load(read_file)
			print ("载入次数time.json成功")
	except:
		init_json()
		print("未发现次数time.json")

#初始化time.json文件
#u次数=0
#h=[名字,次数]
def init_json():
	global h
	u=list("0"*len(names))
	h=dict(zip(names,u))

#显示快速变动的名字
#p=1时执行切换名字
#p=0时显示"我是名字"
def show():
	while (p==1):
		d=show_dog(names)
		label1.config(text=d)
		time.sleep(0.01)
	label1.config(text="我是名字")

#判断nolucky是否有剩
#抽人+抽取延迟间隔

def choice():
	for i in range(s1.get()):
		if (len(nolucky))==0:
			rest_nolucky()
		a_b=a_or_b()
		if a_b==1:
			choice_alreadydog(superlucky)
			add_super_no()
		else:
			choice_noluckydog(nolucky)
			add_super_no()
		label2.config (text="当前抽取 "+str(len(lucky_dogs))+" 人", )
		time.sleep(s2.get())
	#抽完以后执行的代码：
	#p=0
	#写入time.json文件
	global p
	p=0
	save_times()
	save_nolucky()
	
def save_times():
	with open("times.json","w") as write_file:
		json.dump(h,write_file)
		print("保存time.json成功")

def save_nolucky():
	global nolucky
	with open("nolucky.json","w") as write_file:
		json.dump(nolucky,write_file)
		print("保存nolucky.json成功")

#执行多线程
def s_dog_c():
	global t1

	t1=threading.Thread(target=show)
	t1.setDaemon(True)
	t1.start()

	t2=threading.Thread(target=choice)
	t2.setDaemon(True)
	t2.start()

	

#按钮1调用事件
#p=1
#开始多线程
def callback():
	if s1.get()>len(names)-len(lucky_dogs):
		print("已经抽完了")
		tk.messagebox.showerror("www别抽了", "已经抽完了")
	else:
		global p
		p=1
		s_dog_c()

#对被抽的次数进行排序
#c=[(名字,次数)*n]并按照次数排序
def pai():
	c=sorted(h.items(),key=lambda item:int(item[1]))
	lb.delete(0,"end")
	for i in c:
		lb.insert("0", str(i))

def bai():
	c=nolucky
	lbz.delete(0,"end")
	for i in c:
		lbz.insert("0",str(i))

#重复整个程序的次数
def cf():
	#创建新的窗口,输入重复次数
	global e1
	global master
	master = tk.Tk()
	tk.Label(master, text="请输入次数：").grid(row=0)
	e1 = tk.Entry(master)
	e1.grid(row=0, column=1, padx=10, pady=5)
	button=tk.Button(master,text="确认",command=fc,width=10).grid(row=1)
	master.mainloop()
#销毁窗口并重复程序
#把时间间隔设置为0
def fc():
	d=int(e1.get())
	s2.set(0)
	master.destroy()
	for i in range(d):
		choice()
		load_nolucky()
		print("已执行"+str(i+1)+"次")

#询问用户是否排序保存
def save_pai():
	d=tk.messagebox.askokcancel("Python Demo", "是否按ID排序？")
	return d
#保存到文件
#u=db中的ID
#q=排序好的ID
#写入i(=q)+bd中的名字
#排序输出和无序输出
def save():
	d=save_pai()
	u=[]
	for i in lucky_dogs:
		u.append(int(db[i]))
	if d==True:
		q=sorted(u)
		print("排序输出")
	else:
		q=u
		print("无序输出")
	try:
		with open (time.strftime("%Y-%m-%d日%H时%M分%S秒"+"抽取结果.txt", time.localtime()) ,"a") as write_file:
			for i in q:
				write_file.write(str(i))
				write_file.write(bd[str(i)]+'\n')

		print("保存成功")
		tk.messagebox.showinfo("消息", "保存成功")
	except:
		print("保存失败")
		tk.messagebox.showerror("错误", "保存失败")
#作者
def zz():
	bing=tk.Tk()
	bing.title("关于作者")
	bing.geometry("400x300")
	labelz=tk.Label(bing,text="啊柄哥", font=("黑体",24))
	labelz.pack()
	buttonz=tk.Button(bing,text="访问网址",width=10,command=w)
	buttonz.pack()

#访问网址
def w():
	url="https://github.com/10-24/advance_random"
	web.open(url)

#初始化
lucky_dogs=[]
load()
load_nolucky()

#窗口设置
root=tk.Tk()
root.title("高级随机抽样ver1.99")
root.geometry(size)

#名字标签
label1 = tk.Label(root,text="我是名字", font=("黑体",24))
label1.place(x=300,y=80,anchor="center")
#人数标签
label2 = tk.Label(root,text="当前抽取 "+"0"+" 人", font=("黑体",24))
label2.place(x=300,y=40,anchor="center")
#按钮1
button1=tk.Button(root,text="抽 我",command=callback,width=10)
button1.place(relx=0.8, rely=0.1, relheight=0.1, relwidth=0.1)
#按钮2
button2=tk.Button(root,text="重复实验",command=cf,width=10)
button2.place(relx=0.8, rely=0.6, relheight=0.08, relwidth=0.08)
#按钮3
button3=tk.Button(root,text="保存到文件",command=save,width=10)
button3.place(relx=0.8, rely=0.4, relheight=0.08, relwidth=0.08)
#按钮4
button4=tk.Button(root,text="关于作者",command=zz,width=10)
button4.place(relx=0.8, rely=0.9, relheight=0.07, relwidth=0.07)
#人数滑动条
s1 = tk.Scale(root, from_=1,to=len(names),orient="horizontal")
s1.set(ren)
s1.place(x=100,y=120,anchor="center")
#延迟滑动条
s2 = tk.Scale(root, from_=0.01, to=1,resolution=0.01,orient="horizontal")
s2.set(sec)
s2.place(x=100,y=160,anchor="center")
# 创建一个空列表
theLB = tk.Listbox(root,font=("黑体",48),width=10)
theLB.place(relx=0.5, rely=0.5, relheight=0.75, anchor="center")
#非洲人列表
lb = tk.Listbox(root,font=("黑体",12))
lb.place(relx=0.08, rely=0.7, relheight=0.6, anchor="center")
#更新非洲人列表
pai()
#欧洲人列表
lbz=tk.Listbox(root,font=("黑体",12),width=8)
lbz.place(relx=0.15, rely=0.7, relheight=0.6, anchor="center")
#更新欧洲人列表
bai()
#标签说明
s1s=tk.Label(root,text="人数")
s1s.place(x=40,y=130,anchor="e")
s2s=tk.Label(root,text="/sec")
s2s.place(x=150,y=170,anchor="w")
lbs=tk.Label(root,text="排行榜",font=("黑体",12))
lbs.place(relx=0.08, rely=0.35, anchor="n")
lbzs=tk.Label(root,text="up池子",font=("黑体",12))
lbzs.place(relx=0.15, rely=0.35, anchor="n")

root.mainloop()


