#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time:    2021-12-14 23:57
# @Author:  geng
# @Email:   yonglonggeng@163.com
# @WeChat:  superior_god
# @File:    utils.py
# @Project: BoxJellyfish
import os
import shutil


def bjf_copy_file(source_path, target_path):
    source_path = os.path.abspath(source_path)
    target_path = os.path.abspath(target_path)

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if os.path.exists(source_path):
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)
                print(src_file)

    print('copy files finished!')
