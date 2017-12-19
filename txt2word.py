#!/usr/bin/env python
# encoding=utf8
# txt2word
"""
project: 原始文件进行切词后存到一个文件中
Author : wuyingjiao(wyj_258@163.com)
Date : 2017/12/19
"""
import os
import sys
import nltk
import string
import re
import jieba

class Txt2Word(object):
    def __init__(self,InputDataPath):
        self.InputDataPath = InputDataPath
        self.AllFiles = []
        self.OutFilename = None
        self.stopkey = []
    def readDir(self,dirPath):
        if dirPath[-1] == '/':
            print("Dirpath cannot be end with /")
            return
        allFiles = []
        if os.path.isdir(dirPath):
            fileList = os.listdir(dirPath)
            for f in fileList:
                f = dirPath + '/'+ f
                if os.path.isdir(f):
                    subFiles = self.readDir(f)
                    allFiles = subFiles + allFiles
                else:
                    allFiles.append(f)
            return allFiles
        else:
            return "Error,not a dir!"
    def MergeDoc(self,allFiles):
        for filename in allFiles:
            print(filename)
            with open(filename,"rb") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.decode('utf-8')
                    #提取时间信息
                    #正则匹配，对文本进行去除数字、字母和特殊符号的处理
                    lineString = re.sub("[\n\.\!\/_\-$%^*(+\"\')]+|[+—()?【】“”！:,;.？、~@#￥%…&*（）]+", " ", line)
                    #调用函数，去停用词
                    #分词
                    #divide training data and test data
                    #data = lineString.split()
                    #for item in data:
                    #    print(item)
    # 删除停用词
    def delstopword(self,line):
        wordList = line.split(' ')
        sentence = ''
        for word in wordList:
            word = word.strip()
            if word not in self.stopkey:
                if word != '\t':
                    sentence += word + " "
        return sentence.strip()
    def SotpWorDic(self):
        self.stopkey = [line.strip() for line in open('E:/code/Machine-Learning/dictionary/stopword.txt', 'r', encoding='utf-8').readlines()]
if __name__ == "__main__":
    txt2word = Txt2Word("E:/code/Machine-Learning/testdata")
    txt2word.SotpWorDic()
    Filelist = txt2word.readDir(txt2word.InputDataPath)
    txt2word.MergeDoc(Filelist)
    txt2word.SotpWorDic()