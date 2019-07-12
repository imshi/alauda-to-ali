#!/usr/bin/python
# coding=utf-8

import modules.kubectl as kubectl
import modules.image as image
from modules.tool import *
import json
# import modules.tmp as tmp

# l = [0,80,20880]
# kubectl_ops = kubectl.kubectl_init("nginx", "docker.io/nginx", l, "default")
# kubectl_ops.kube_controller()

def sync_image(app_name, app_image, dest_url):
    image_ops = image.docker_init(app_name, app_image, dest_url)
    image_ops.docker_controller()

def update_app(app_name, app_image, port_list, app_namespace):
    kubectl_ops = kubectl.kubectl_init(app_name, app_image, port_list, app_namespace)
    kubectl_ops.kube_controller()

def main():
    sync_image("api-tsp-command-service", "testing-clusers-hbykt.customerindex.alauda.cn:5000/api-tsp-command-service:tag_6", "registry-vpc.cn-hangzhou.aliyuncs.com/ecarx-app/api-tsp-command-service:tag_6")
    # ######do all
    # with open("list.json", 'r') as f:
    #     app_dict = json.load(f)
    #     for key in app_dict:
    #         app_name = key
    #         app_image = app_dict[key]["Image"]
    #         tag = app_image.split(':')[2]
    #         dest_url = ali_registry + app_name + ":" + tag
    #         port_list = app_dict[key]["Port"]
    #         sync_image(app_name, app_image, dest_url)
    #         update_app(app_name, app_image, port_list, app_namespace)

if __name__ == '__main__':
    main()