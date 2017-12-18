#!/usr/bin/env python
# encoding=utf8
# CNER
"""
project: Clinical Named Entity Recognition
Author : wuyingjiao(wyj_258@163.com)
Date : 2017/12/17
"""
import sys
import sklearn
import numpy
from sklearn import svm
import scipy
import pandas
import matplotlib
import gensim
import tensorflow
class CNER(object):
    def __init__(self,InputFilename,OutFilename):
        self.InputFilename = InputFilename
        self.OutFilename = OutFilename
    #文件读入字典里存储
    def txt2res(self):
        pass
    def svmclassifier(self):
        pass
if __name__ == "__main__":
    csnr = CNER("in.txt","out.txt")
    csnr.txt2res()
    csnr.svmclassifier()
    print("hello ml!")