# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 10:01:58 2021

@author: Lychee
"""
import numpy as np
import matplotlib.pyplot as plt
import random

def update(w,b,x,y,lr):
    """
    更新参数
    损失函数为L(w,b) = -sum((w*x+b)*y) x属于误分类点集
    """
    w = w + lr*x*y
    b = b + lr*y
    print(w,b)
    return w,b

def judge(w,b,x,y):
    """
    判断数据 x 是否是误分类点
    判断标准即 (w*x+b)*y < 0 则为误分类点
    """
    flag = (sum(w*x)+b)*y
    if flag<=0:
        return False
    else:
        return True

def getErrorPoint(x, y, w, b):
    """
    遍历所有训练数据，获取误分类点集
    """
    count = 0
    for i in range(len(x)):
        if not judge(w,b,x[i],y[i]):
            if count == 0:
                Point = np.array([x[i]])
                label = np.array([y[i]])
                count += 1
            else:
                Point = np.append(Point, [x[i]], axis=0)
                label = np.append(label, y[i])
    if count==0:
        return np.array([[]]),np.array([[]])
    return Point, label

if __name__=="__main__":
    # 训练数据
    x = np.array([[3,3],[4,3],[1,1],[7,8],[2,5],[4,5]])
    y = np.array([1,1,-1,1,-1,-1])
    x_lim = 10
    y_lim = 10
    # 权重初始化
    w = np.array([0,0])
    # 偏差初始化
    b = 0
    # 学习率 0 < lr <= 1
    lr = 0.5
    
    # 训练
    Point, label = getErrorPoint(x,y,w,b)
    while Point.size:
        i = random.randint(0, len(Point)-1)
        w,b = update(w,b,Point[i],label[i],lr)
        Point,label = getErrorPoint(x,y,w,b)
    
    # 绘制训练数据散点图
    plt.close()
    for i in range(len(x)):
        plt.scatter(x[:,0],x[:,1])
    # 绘制最终的分类超平面
    if w[1]!=0 and w[0]!=0:
        px = np.linspace(0,x_lim,100)
        py = -(w[0]*px+b)/w[1]
        plt.plot(px,py)
    elif w[1]==0 and w[0]!=0:
        plt.axvline(-b/w[0])
    else:
        plt.axhline(-b/w[1])
    plt.ylim([0,y_lim])
    plt.xlim([0,x_lim])
