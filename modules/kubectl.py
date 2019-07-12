#!/usr/bin/python
# coding=utf-8

from .tool import *
# import re
from jinja2 import Template, Environment, FileSystemLoader
import urllib3
from kubernetes import client, config
import yaml
from pprint import pprint

urllib3.disable_warnings()


class kubectl_init(object):
    def __init__(self, app_name, app_image, app_port_list, namespace):
        self.app_name = app_name
        self.app_image = app_image
        self.namespace = namespace
        if 0 in app_port_list:
            app_port_list.remove(0)
        app_port_list.sort()
        self.app_port_list = app_port_list
        self.app_yaml_dir = app_yaml_dir
        self.app_j2_dir = app_j2_dir
    def dep_yaml_j2(self, app_name):
        # f_rc = APP_YAML_DIR + self.app_name + '_yaml/' + self.app_name + '_deployment.yaml'
        deployment_file = os.path.join(app_yaml_dir, self.app_name + '_deployment.yaml')
        # print(deployment_file)
        # print(self.app_j2_dir)
        env = Environment(loader=FileSystemLoader(self.app_j2_dir, 'utf-8'))
        template = env.get_template(j2_tempalte)
        deployment = template.render(name=self.app_name, namespace=self.namespace, image=self.app_image, port=self.app_port_list[0])
        # with open(os.path.join(self.app_j2_dir, j2_tempalte), "r") as fd:
        #     template = Template(fd.read())
        #     deployment = template.render(name=self.app_name, image=self.app_image, port=self.app_port_list[0])
        with open(deployment_file, 'w') as f:
            f.write(deployment)
        return deployment_file

    def svc_yaml_j2(self, app_name, app_port_list):
        if len(self.app_port_list) == 1:
            print("One port, use service.js")
            j2_tempalte = 'service.j2'
            service_file = os.path.join(app_yaml_dir, self.app_name + '_service.yaml')
            env = Environment(loader=FileSystemLoader(self.app_j2_dir, 'utf-8'))
            template = env.get_template(j2_tempalte)
            service = template.render(name=app_name, namespace=self.namespace, port=app_port_list[0])
            with open(service_file, 'w') as f:
                f.write(service)
        elif len(self.app_port_list) == 2:
            print("Two port, use service-two.js")
            j2_tempalte = 'service-two.j2'
            service_file = os.path.join(app_yaml_dir, self.app_name + '_service.yaml')
            env = Environment(loader=FileSystemLoader(self.app_j2_dir, 'utf-8'))
            template = env.get_template(j2_tempalte)
            service = template.render(name=app_name, namespace=self.namespace, port01=app_port_list[0], port02=app_port_list[1])
            with open(service_file, 'w') as f:
                f.write(service)
        else:
            print("Service Count Error")
            return None
        return service_file

    def kube_get_dep_list(self, api_instance):
        api_response = api_instance.list_namespaced_deployment(self.namespace)
        deployment_list = []
        for i in api_response.items:
            deployment_list.append(i.metadata.name)
        return deployment_list

    def kube_create_dep(self, api_instance):
        print(self.app_port_list[0])
        deplayment_file = self.dep_yaml_j2(self.app_name)
        with open(deplayment_file, 'r') as f:
            dep = yaml.load(f)
            api_response = api_instance.create_namespaced_deployment(
                body=dep, namespace=self.namespace)
            print("Deployment created. status='%s'" % str(api_response.status))

    def kube_replace_dep(self, api_instance):
        deployment_file = self.dep_yaml_j2(self.app_name)
        with open(deployment_file, 'r') as f:
            dep = yaml.load(f)
            api_response = api_instance.replace_namespaced_deployment(
                name=self.app_name, namespace=self.namespace, body=dep)
            print("Deployment status:", api_response.status.conditions[0].status)
            # pprint(api_response.status.conditions[0].status)

    def kube_get_svc_list(self, api_instance):
        api_response = api_instance.list_namespaced_service(
            namespace=self.namespace)
        service_list = []
        for i in api_response.items:
            service_list.append(i.metadata.name)
        return service_list

    def kube_create_svc(self, api_instance):
        service_file = self.svc_yaml_j2(self.app_name, self.app_port_list)
        if service_file:
            with open(service_file, 'r') as f:
                svc = yaml.load(f)
                api_response = api_instance.create_namespaced_service(
                    namespace=self.namespace, body=svc)
                print("Service created. status='%s'" % str(api_response.status))

    def kube_replace_svc(self, api_instance):
        service_file = self.svc_yaml_j2(self.app_name, self.app_port_list)
        with open(service_file, 'r') as f:
            svc = yaml.load(f)
            api_response = api_instance.replace_namespaced_service(
                name=self.app_name, namespace=self.namespace, body=svc)
            print("Service updated. status='%s'" % str(api_response.status))

    def kube_controller(self):
        # configuration = client.Configuration()
        # configuration.host = "https://c5b1d0b4a27474d47adeeb5132a397197.k8s-g1.cn-hangzhou.aliyuncs.com:6443"
        # configuration.verify_ssl = False
        # client.Configuration.set_default(configuration)
        config.load_kube_config()
        k8s_beta = client.AppsV1beta2Api()
        k8s_core = client.CoreV1Api()
        # deployment_list = self.kube_get_dep_list(k8s_beta)
        # return deployment_list

        # 处理deployment
        deployment_list = self.kube_get_dep_list(k8s_beta)
        if self.app_name in deployment_list:
            print("Deployment already exists, replace ...")
            try:
                self.kube_replace_dep(k8s_beta)
            except Exception as e:
                print("Deployment replace Failed!, message:")
                print(e)
        else:
            print("Deployment not exists, creat ...")
            try:
                self.kube_create_dep(k8s_beta)
            except Exception as e:
                print("Deployment create Failed! message:")
                print(e)

        # 处理Service
        # svc = v1.list_namespaced_service(namespace=self.namespace)
        # for i in svc.items:
        #     if re.search():
        #         pass
        service_list = self.kube_get_svc_list(k8s_core)
        if self.app_name in service_list:
            print("Service already exists, if not necessary, do not change!")
        else:
            print("None Services exists, create")
            try:
                self.kube_create_svc(k8s_core)
            except Exception as e:
                print("Service create Failed! message:")
                print(e)