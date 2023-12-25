# GreenWorld
2023数媒基课设

## 项目说明
### 什么是GreenWorld？

GreenWorld是一个利用数字媒体中文本、图像、音频、视频相关处理技术及 Web 开发技术，
旨在提供关于生态系统、生物多样性、环境保护等方面的知识。通过生动的视觉和听觉呈现，
这个系统能够有效地传达生态环境的复杂性和对人类生活的重要性。

## 安装项目
### 后端
```bash
# clone 项目
git clone https://github.com/434ROOM/green-world.git
# 切换目录
cd green-world
# 安装依赖
pip install -r ./requirements.txt
# 更新数据库
python manage.py migrate
# 运行后端（dev or Production）
python manage.py runserver
``` 

### 前端
```bash
# 切换目录
cd green-world
cd app-front
# 安装依赖
npm install
# 修改配置文件 src/serverConfig.js
...
# 运行前端（dev）
npm run dev
# 打包生产文件（Production）
npm run build
# 部署 dist 文件夹（Production）
...
```

## 运行环境
python + Node.js

## 项目结构

Django + vue（Ant Design Vue）

## 分支说明
- main: 主分支，用于发布版本

不能直接push，只能接受其他分支的PR

- service-core: 后端分支，用于开发后端

可以直接push

- app-front: 前端分支，用于开发前端

可以直接push
