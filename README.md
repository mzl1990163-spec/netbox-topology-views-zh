# NetBox 拓扑视图插件(中文汉化二次开发版)

基于 [netbox-topology-views](https://github.com/mattieserver/netbox-topology-views) **v4.5.1**(Apache-2.0)二次开发,在保留上游全部能力的基础上做了界面汉化和功能增强,并内置 8 组共 **256 个华三(H3C)网络设备图标**。

已在 **NetBox 4.6.8(netbox-docker 5.0.2)** 上部署验证。

## 功能特性

- **实时拓扑**:根据设备间线缆自动生成拓扑图,支持按名称 / 站点 / 标签 / 角色过滤,支持导出 XML(draw.io/diagrams.net)与 PNG。
- **我的拓扑**:保存当前过滤器与坐标布局,一键回到常用视图(顶部菜单「拓扑 → 我的拓扑」)。
- **图标设置**(全新改造的配置页):
  - 网页直接上传图标,支持 png / svg / jpg / gif / webp / bmp,单文件 ≤ 2MB,支持多选;
  - **图标分组**:内置组 + 自定义分组(对应图标目录下的子目录),分组下拉统一管理;
  - **新建分组**:网页一键创建(组名仅允许字母 / 数字 / - / _),刷新后持久保留;
  - **列表式配置**:每个设备角色一行,分组下拉 + 图标选择弹层,点击「保存」即生效。
- **角色图标绑定**:设备角色 ↔ 图标一一对应,拓扑图中按角色展示对应设备图标。

## 与上游的差异

| 上游 v4.5.1 | 本分支 |
| --- | --- |
| 英文界面 | 全中文界面(菜单 / 页面 / 按钮 / 角色名) |
| 无图标管理页面 | 图标设置页:上传 / 分组 / 新建分组 / 列表式配置 |
| 仅内置默认图标 | 内置 8 组 256 个华三图标 + 49 个默认图标 |
| 保存视图入口较弱 | 新增「我的拓扑」菜单 |
| 含 PyPI 发布工作流 | 已移除(避免误发布) |

## 图标目录结构

图标按分组子目录存放在 `netbox_topology_views/static/netbox_topology_views/img/`:

```
img/
├── 根目录:内置默认图标(49 个 svg)
├── h3c-switch/            25 个  (Switch-01~25)
├── h3c-router/            23 个  (router-01~23)
├── h3c-wireless/          29 个  (wireless-01~29)
├── h3c-security/          16 个  (security-01~16)
├── h3c-VideoSurveillance/ 41 个  (VideoSurveillance-01~41)
├── h3c-others/            69 个  (other-01~69)
├── h3c-storage/           44 个  (storage-01~44)
└── h3c-service-software/   9 个  (service-01~09)
```

> 根目录即「内置」分组;每个子目录对应一个自定义分组。网页新建分组 = 在该目录下创建子目录。

---

# 快速部署(镜像版 v1.0.1)

> 给**第一次接触本项目的人**。按下面命令一条条执行,全程约 5 分钟,不需要懂 NetBox 源码或插件开发。

## 这是什么

本项目把以下三样东西打包成了一个 Docker 镜像,直接拉来用:

| 内容 | 说明 |
|------|------|
| **NetBox 4.6.8** | 网络设备管理平台(开源) |
| **拓扑插件 `netbox_topology_views`(中文汉化版)** | 从 NetBox 的设备 + 线缆自动生成网络拓扑图,并提供「我的拓扑」「图标设置」等中文功能 |
| **8 组共 256 个华三(H3C)网络设备图标** + 49 个默认图标 | 给"交换机 / 路由器 / 防火墙 / AP / 服务器"等角色用 |

打包好的镜像地址(公开,免登录):`ghcr.io/mzl1990163-spec/netbox-topology-views-zh:1.0.1`

## 部署文件从哪来

部署只需要 2 个小文件,**都不用自己写**:

| 文件 | 从哪来 | 干什么 |
|------|------|------|
| `compose.image.yml` | 本项目仓库的 `deploy/` 目录(下面用 wget 直接下载) | Docker 编排文件:告诉 Docker 用什么镜像、什么端口、什么环境变量 |
| `configuration/plugins.py` | 自己创建(下面有一行命令) | 一行配置 `PLUGINS = ["netbox_topology_views"]`,意思是"启用这个插件" |

> `netbox_topology_views` 是**这个插件的名字**。

部署时 Docker 会自动从 **ghcr.io(GitHub 容器镜像仓库)** 拉取打包好的镜像(里面有 NetBox + 插件 + 256 图标),**不用拉源码、不用自己构建**。

## 准备

- 一台 **Ubuntu 22.04 / 24.04** 服务器,有 **sudo** 权限
- 能访问 **GitHub** 和 **ghcr.io**(都是公开的,免登录)

## 部署步骤(一条一条执行)

### 第 1 步:安装 Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
```

> **做什么**:装 Docker 引擎(跑容器)和 Docker Compose v2(编排多个容器)。
> **验证**:
> ```bash
> docker --version        # 应显示版本号
> docker compose version
> ```

### 第 2 步:创建部署目录

```bash
sudo mkdir -p /opt/my-netbox/configuration
cd /opt/my-netbox
```

> **做什么**:在服务器上建一个工作目录,放部署文件。`/opt/my-netbox` 是项目名(可改成你喜欢的名字,保持后续命令一致即可)。

### 第 3 步:下载 / 创建部署文件

```bash
# 从本项目 GitHub 仓库下载 compose 文件
sudo wget -O compose.image.yml \
  https://raw.githubusercontent.com/mzl1990163-spec/netbox-topology-views-zh/main/deploy/compose.image.yml

# 创建插件启用配置(就一行:启用 netbox_topology_views 插件)
echo 'PLUGINS = ["netbox_topology_views"]' | sudo tee configuration/plugins.py
```

> **验证**:
> ```bash
> ls -la /opt/my-netbox/
> # 应有: compose.image.yml 和 configuration/ 目录
> cat /opt/my-netbox/configuration/plugins.py
> # 应输出: PLUGINS = ["netbox_topology_views"]
> ```

### 第 4 步:启动

```bash
sudo docker compose -f compose.image.yml up -d
```

> **做什么**:Docker 读 `compose.image.yml`,从 ghcr.io 拉取镜像,启动 6 个容器:netbox(主服务,网页 8000 端口)、netbox-worker / netbox-housekeeping(后台任务)、postgres / redis / redis-cache(数据库和缓存)。`up -d` 表示后台运行。
> **验证**(应看到 6 个容器都 Started):
> ```bash
> sudo docker compose -f compose.image.yml ps
> ```

### 第 5 步:等 NetBox 就绪(约 1-2 分钟)

```bash
curl -sI http://127.0.0.1:8000/ | head -1
```

> **期望输出**:`HTTP/1.1 302 Found`(NetBox 已就绪,把没登录的请求跳转到登录页)。
> 5 分钟还没就绪就看日志:
> ```bash
> sudo docker compose -f compose.image.yml logs netbox | tail -30
> ```

### 第 6 步:填充图标(首次部署必须执行!)

```bash
sudo docker compose -f compose.image.yml exec netbox \
  python3 /opt/netbox/netbox/manage.py collectstatic --no-input
```

> **做什么**:NetBox 启动时不会自动把插件的 256 个图标复制到图标卷(已知限制),这条命令手动把镜像里的图标"铺"到图标卷。
> **期望输出**:`N static files copied`(`N` 大约 300+,含 256 个图标)。

### 第 7 步:验证

```bash
# 图标卷应有 57 个内置图标 + 8 个分组目录
sudo ls /opt/my-netbox/icons/ | head
sudo ls -d /opt/my-netbox/icons/*/ | head

# 所有 6 个容器都应 Up
sudo docker compose -f compose.image.yml ps
```

### 第 8 步:浏览器访问

打开 **`http://<服务器IP>:8000`**,登录:

- 账号:**`admin`**
- 密码:**`123456`**

进去后:
- 顶部应有 **「拓扑」** 菜单(含「实时拓扑」「我的拓扑」)
- 「偏好设置 → 图标设置」应有 **8 个分组共 256 个华三图标** —— 部署成功

## 常见问题

**Q: 浏览器打不开 8000 端口**
- 检查防火墙:`sudo ufw allow 8000`
- 检查容器是否都在 Up:`sudo docker compose -f compose.image.yml ps`

**Q: 图标设置是空的(没有图标)**
- 第 6 步的 `collectstatic` 没执行,再跑一次。

**Q: 想换端口(8000 → 别的)**
- 编辑 `compose.image.yml` 里 `ports: - "8000:8080"`,改左边的 `8000`(右边的 8080 是容器内部端口,别动)。

**Q: 以后更新版本(如 1.0.1 → 1.0.2)**
- 编辑 `compose.image.yml`,把 `image:` 末尾的 `1.0.1` 改成新版本号
- `sudo docker compose -f compose.image.yml up -d`

**Q: 出错了怎么看日志**
```bash
sudo docker compose -f compose.image.yml logs netbox | tail -50
```

## 源码部署(备选,自行构建)

适合想自己构建镜像的场景,详细步骤见 [docs/DEPLOY.md](docs/DEPLOY.md)。仓库 `deploy/` 已提供现成文件:

- `deploy.sh` — 一键脚本(克隆 netbox-docker → 放插件 → 构建 → 启动)
- `Dockerfile-Plugins` — 锁定基础镜像 `ghcr.io/netbox-community/netbox:v4.6.8-5.0.2`
- `docker-compose.override.yml` — icons 持久卷挂载

## License

- 插件本体:Apache-2.0(保留上游版权)。
- 内置默认图标集:CC BY-SA 4.0(见 `netbox_topology_views/static/netbox_topology_views/img/LICENSE`)。
- 华三(H3C)设备图标版权归新华三集团所有,仅限内部使用,请勿公开分发。

## 致谢

- 上游项目:[netbox-topology-views](https://github.com/mattieserver/netbox-topology-views)(作者 Mattijs Vanhaverbeke,Apache-2.0)
- [netbox-docker](https://github.com/netbox-community/netbox-docker) 部署方案
