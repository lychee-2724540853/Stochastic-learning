# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 21:39:06 2021

@author: Lychee
"""
from KDTree import KDTree as KDTree
import numpy as np
import matplotlib.pyplot as plt

# 输入数据
input_data = np.array([[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]])

# 构造 KD树
root = KDTree(input_data, 0)

# tree 保存 KD树的前向遍历   在此处无用
tree = []
root.forwordTree(tree)

# 给定目标点
point = [8,3.9]
# 寻找 KD树 中目标点的最近邻
x = root.searchKNeibor(point)

# 绘图
plt.close()
plt.scatter(input_data[:,0],input_data[:,1])
#for point in tree:
#    if point["axis"]==0:
#        plt.axvline(point["point"][0])
#    else:
#        plt.axhline(point["point"][1])
plt.grid(True)
plt.scatter(point[0],point[1])
# 连接目标点和最近邻
plt.plot([x.key[0],point[0]],[x.key[1],point[1]], color='r')