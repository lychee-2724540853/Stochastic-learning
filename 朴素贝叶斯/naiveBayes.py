# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:31:48 2021

@author: Lychee
"""
import numpy as np
import json
import os

def read_csv(file, delimeter=','):
    datas = open(file,'r', encoding='utf-8')
    inputs = []
    labels = []
    for data in datas:
        data = data.strip()
        data = data.split(delimeter)
        inputs.append(data[0].split(' '))
        labels.append(int(data[1]))
    
    return inputs, labels

class BayesModel():
    def __init__(self, inputs, labels, lamda=0):
        """
        inputs: 输入向量的特征值矩阵，如:
            [[1,2,3],['L','M','S']]
        表示输入的第一个特征取值范围是{1,2,3},第二个特征的取值范围{'L','M','S'}
        labels: 类别集合
        lamda: Bayes估计系数，取0即为极大似然估计
        """
        self.inputs = inputs
        self.labels = labels
        self.lamda = lamda
        self.initBayes()
                    
    def load_train_data(self, train_inputs, train_labels):
        self.train_inputs = np.array(train_inputs)
        self.train_labels = np.array([str(label) for label in train_labels])
    
    def initBayes(self):
        self.Bayes = {}
        for label in self.labels:
            self.Bayes[label] = {}
            self.Bayes[label]['probility'] = 0.0
            for i in range(len(self.inputs)):
                self.Bayes[label][i] = {}
                for j in range(len(self.inputs[i])):
                    self.Bayes[label][i][self.inputs[i][j]] = 0
    def train(self):
        self.initBayes()
        for label in self.labels:
            count = sum(self.train_labels==label)
            self.Bayes[label]['count'] = float(count)
            self.Bayes[label]['probility'] = (self.Bayes[label]['count']+self.lamda)/(len(self.train_labels)+len(self.inputs)*self.lamda)
        for label in self.labels:
            for i in range(len(self.inputs)):
                for j in range(len(self.inputs[i])):
                    self.Bayes[label][i][self.inputs[i][j]] = (self.lamda)/(self.Bayes[label]['count'] + len(self.inputs[i])*self.lamda)
        for j in range(np.size(self.train_inputs, 0)):
            label = self.train_labels[j]
            for i, c in enumerate(self.train_inputs[j]):
                self.Bayes[label][i][c] += (1.0)/(self.Bayes[label]['count'] + len(self.inputs[i])*self.lamda)
        
        return self.Bayes
    
    def saveModel(self):
        model = open("model.json", 'w', encoding='utf-8')
        json.dump(self.Bayes, model, ensure_ascii=False)
    
    def loadModel(self):
        if os.path.exists("model.json"):
            with open("model.json",'r') as fp:
                self.Bayes = json.load(fp,)
                return self.Bayes
        else:
            raise Exception("model path does not exist!")
    
    def predict(self, inputs):
        probility = [1]*len(self.labels)
        for i, label in enumerate(self.labels):
            probility[i] = self.Bayes[label]['probility']
            for induce, x in enumerate(inputs):
                probility[i] *= self.Bayes[label][induce][x]
        label = np.argmax(probility)
        return self.labels[label], probility
    
    
data_path = "data.txt"
labels = ['-1', '1']
inputs = [['1','2','3'],['M','S','L']]
train_inputs, train_labels = read_csv(data_path)
model = BayesModel(inputs, labels, 0)
model.load_train_data(train_inputs, train_labels)
Bayes = model.loadModel()
Bayes = model.train()
model.saveModel()
print(model.predict(['2','S']))
