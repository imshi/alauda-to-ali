#!/usr/bin/python
# coding=utf-8
import docker
from .tool import *
# import os
# import shutil
# from git import Repo
# from io import BytesIO

class docker_init(object):
    def __init__(self, app_name, source_url, dest_url):
        self.app_name = app_name
        self.source_url = source_url
        self.dest_url = dest_url

    def docker_pull(self):
        try:
            client = docker.from_env(version="auto")
            print(self.app_name)
            client.pull(self.source_url)
        except Exception as identifier:
            print("Docker image pull failed ! ERROR INFO: \n")
            print(identifier)

    def docker_push(self):
        try:
            client = docker.from_env(version="auto")
            print(self.app_name)
            ################### 打tag #############
            client.tag(self.source_url, self.dest_url)
            client.push(self.dest_url)
            #result = client.push(self.image_with_tag)
            #print(result)
        except Exception as identifier:
            print("Docker image push failed ! ERROR INFO: \n")
            print(identifier)

    def docker_remove(self):
        try:
            client = docker.from_env(version="auto")
            client.remove_image(image=self.dest_url)
            client.remove_image(image=self.source_url)
        except Exception as identifier:
            print("Docker image remove failed ! ERROR INFO: \n")
            print(identifier)

    def docker_controller(self):
        # 构建docker镜像
        print("===== Start to pull images ... ")
        self.docker_pull()
        # 推送镜像至仓库
        print("===== Start to push images ... ")
        self.docker_push()
        # 清理本地镜像
        print("===== Start to clean local images ... ")
        self.docker_remove()


# client = docker.from_env(version="auto")
# client = docker.DockerClient(base_url='unix://var/run/docker.sock',version="auto")

