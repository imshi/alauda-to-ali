### 用于灵雀云k8s项目迁移至阿里云
#### 部分说明：
- 拉取灵雀云数据并重组，存储至本地使用golang实现（均为内置模块）；
- 镜像同步及服务同步使用Python实现（相关依赖参见requirements.txt文件）；

### 使用：
- golang1.11 + 及 python3.6+环境
- 安装依赖：`pip install -r requirements.txt`
- 获取灵雀云数据（自行填充Token认证数据）：`go run alauda.go`
- 同步镜像、服务至阿里云：`python app_main.py`