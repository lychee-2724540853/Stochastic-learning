# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 21:39:06 2021

@author: Lychee
"""
from KDTree import KDTree, KNearestNeibor
import numpy as np
import matplotlib.pyplot as plt

# 输入数据
input_data = np.array([[2,3,1],[5,4,1],[9,6,1],[4,7,1],[8,1,1],[7,2,1]])
# 给定目标点
point = [7.1,4,1]
# 构造 KD树
#root = KDTree(input_data)
root = KNearestNeibor(input_data)

# 寻找 KD树 中目标点的最近邻
#leaf = root.searchNeibor(point)
leafs = root.searchNeibors(point,4)

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
for leaf in leafs:
    plt.plot([leaf[0],point[0]],[leaf[1],point[1]], color='r')
