#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time:    2021-12-15 00:17
# @Author:  geng
# @Email:   yonglonggeng@163.com
# @WeChat:  superior_god
# @File:    Build.py
# @Project: BoxJellyfish
import pickle


class BJFTask(object):
    def __init__(self):
        # load_model_method
        f = open('resultStages/artifacts/model.pkl', 'rb')
        self.object_model = pickle.load(f)

    #     self.load_model(object_model)
    #
    def load_model(self):
        return self.object_model

    def predict(self, data, data2):
        return self.object_model.predict(data, data2)


def get_model():
    f = open('resultStages/artifacts/model.pkl', 'rb')
    return pickle.load(f)


def predict(object_model, data, data2):
    return object_model.predict(data, data2)


if __name__ == '__main__':
    model = get_model()
    predict(model, 1, 2)
