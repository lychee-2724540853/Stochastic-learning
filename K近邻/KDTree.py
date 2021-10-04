# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 15:49:57 2021

@author: Lychee
"""

import numpy as np
import math

class KDTree():
    def __init__(self, value, depth, parent=None):
        """
        value: KDTree 下的所有节点的集合
        depth: 当前节点的深度
        """
        self.parent = parent
        self.left = None
        self.right = None
        self.depth = depth
        self.dim = np.size(value, 1)
        self.axis = int(np.floor(self.depth%self.dim))
        self.tree = value[np.argsort(value[:,self.axis])]
        self.length = np.size(self.tree, 0)
        self.induce = int(np.floor(self.length/2))
        #self.key = None
        if self.length>=1:
            self.key = self.tree[self.induce]
            if self.induce>0:
                self.left = KDTree(self.tree[0:self.induce], self.depth+1, self)
            if self.induce+1<self.length:
                self.right = KDTree(self.tree[self.induce+1:], self.depth+1, self)
                
#    def insertLeft(self, key):
#        if self.left==None:
#            self.left = KDTree(key)
#        else:
#            raise Exception("当前节点已存在左子节点，无法插入!")
#        return self.left
#    
#    def insertRight(self, key):
#        if self.right==None:
#            self.right = KDTree(key)
#        else:
#            raise Exception("当前节点已存在右子节点，无法插入!")
#        return self.right
    
    # 中间遍历
    def middleTree(self):
        if self.left:
            self.left.forwordTree()
        print(self.key)
        if self.right:
            self.right.forwordTree()
    # 前向遍历
    def forwordTree(self, output):
        output.append({"point": self.key, "axis":self.axis})
        if self.left:
            self.left.forwordTree(output)
        if self.right:
            self.right.forwordTree(output)
    # 后向遍历
    def backwordTree(self):
        if self.left:
            self.left.forwordTree()
        if self.right:
            self.right.forwordTree()
        print(self.key)

    # 返回左节点
    def getLeft(self):
        return self.left
    
    # 返回右节点
    def getRight(self):
        return self.right
    
    # 返回父节点
    def getParent(self):
        return self.parent
    
    # 返回指定值的节点
    def getNode(self, node):
        if (self.key == node).all():
                return self
        if self.left:
            temp = self.left.getNode(node)
            if temp:
                return temp
        if self.right:
            temp = self.right.getNode(node)
            if temp:
                return temp
    
    # 返回兄弟节点
    def getBro(self):
        parent = self.getParent()
        right = parent.right
        left = parent.left
        
        if right and (right.key == self.key).all():
            return left
        else:
            return right
        
    # 返回 给定点 的最近邻 叶子节点
    def findNeibor(self, point):
        if point[self.axis] < self.key[self.axis]:
            if self.left:
                return self.left.findNeibor(point)
            else:
                return self
        else:
            if self.right:
                return self.right.findNeibor(point)
            else:
                return self
    # 返回KD树中 给定点的 最近邻 节点
    def searchKNeibor(self, point):
        leaf = self.findNeibor(point)
        current = leaf

        while current != self:
            parent = current.getParent()
            
            distanceOfleaf = 0
            for i in range(len(leaf.key)):
                distanceOfleaf += (leaf.key[i] - point[i])**2
            distanceOfleaf = math.sqrt(distanceOfleaf)
            
            distanceOfparent = 0
            for i in range(len(parent.key)):
                distanceOfparent += (parent.key[i] - point[i])**2
            distanceOfparent = math.sqrt(distanceOfparent)
            
            if distanceOfparent < distanceOfleaf:
                leaf = parent
                distanceOfbro = 0 
                bro = current.getBro()
                if bro:
                    for i in range(len(bro.key)):
                        distanceOfbro += (bro.key[i] - point[i])**2
                    distanceOfbro = math.sqrt(distanceOfbro)
          
                    if distanceOfbro < distanceOfparent:
                        leaf = bro.searchKNeibor(point)

            current = parent
        return leaf