# 快速部署指南(镜像版 v1.0.1)

> 给**第一次接触本项目的人**。按下面命令一条条执行,全程约 5 分钟,不需要懂 NetBox 源码或插件开发。

---

## 0. 这是什么

本项目把以下三样东西打包成了一个 Docker 镜像,可以直接拉来用:

| 内容 | 说明 |
|------|------|
| **NetBox 4.6.8** | 网络设备管理平台(开源,类似简化版的 CMDB) |
| **拓扑插件 `netbox_topology_views`(中文汉化版)** | 自动从 NetBox 的设备+线缆生成网络拓扑图,并提供「我的拓扑」「图标设置」等中文功能 |
| **8 组共 256 个华三(H3C)网络设备图标** + 49 个默认图标 | 直接给"交换机/路由器/防火墙/AP/服务器"等角色用 |

打包好的镜像地址(公开,免登录):`ghcr.io/mzl1990163-spec/netbox-topology-views-zh:1.0.1`

---

## 1. 这些文件是哪来的

部署只需要 2 个小文件,**都不用自己写**:

| 文件 | 从哪来 | 干什么 |
|------|------|------|
| `compose.image.yml` | 本项目 **GitHub 仓库** 的 `deploy/` 目录 | Docker 编排文件:告诉 Docker 用什么镜像、什么端口、什么环境变量 |
| `configuration/plugins.py` | 自己创建(下面会给一行命令) | 一行配置 `PLUGINS = ["netbox_topology_views"]`,意思是"启用这个插件" |

> `netbox_topology_views` 是**这个插件的名字**(每个 NetBox 插件都有唯一名字)。

部署期间还会自动从 **ghcr.io(GitHub 容器镜像仓库)** 拉取我们打包好的镜像(里面已经有 NetBox + 插件 + 256 图标),**你不用拉源码、也不用自己构建**。

---

## 2. 准备

- 一台 **Ubuntu 22.04 / 24.04** 服务器,有 **sudo** 权限
- 能访问 **GitHub** 和 **ghcr.io**(两者都是公开的,免登录)
- 可选:如果要恢复另一台服务器的数据,需要知道那台的 `SECRET_KEY`(见第 4 步)

---

## 3. 部署步骤

> 每条命令下面都有**注释说明它在做什么、期望看到什么**。照着敲,出问题把输出发我。

### 第 1 步:安装 Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
```

> **做什么**:装 Docker 引擎(用来跑容器)和 Docker Compose v2(用来编排多个容器一起启动)。
> **验证**:
> ```bash
> docker --version        # 应显示版本号
> docker compose version
> ```

### 第 2 步:创建部署目录

```bash
sudo mkdir -p /opt/netbox-mzl/configuration
cd /opt/netbox-mzl
```

> **做什么**:在服务器上建一个工作目录,放部署文件。`/opt/netbox-mzl` 是项目名(你可以改成 `netbox` 之类,只要一致就行)。

### 第 3 步:下载/创建部署文件

```bash
# 从 GitHub 仓库下载 compose 文件(就是本项目 deploy/ 目录里那个)
sudo wget -O compose.image.yml \
  https://raw.githubusercontent.com/mzl1990163-spec/netbox-topology-views-zh/main/deploy/compose.image.yml

# 创建插件启用配置(就一行:告诉 NetBox 启用 netbox_topology_views 这个插件)
echo 'PLUGINS = ["netbox_topology_views"]' | sudo tee configuration/plugins.py
```

> **compose.image.yml** 不是你自己写的,是从本项目 GitHub 仓库的 `deploy/` 目录直接下载的。**plugins.py** 是上面那条 `echo` 命令直接生成的(就一行内容)。

> **验证**:
> ```bash
> ls -la /opt/netbox-mzl/
> # 应有: compose.image.yml  和  configuration/ 目录
> cat /opt/netbox-mzl/configuration/plugins.py
> # 应输出: PLUGINS = ["netbox_topology_views"]
> ```

### 第 4 步:修改 SECRET_KEY(关键!)

```bash
sudo nano compose.image.yml
```

在打开的文件里找到这一行:

```yaml
SECRET_KEY: "改成与源服务器一致的SECRET_KEY"
```

**SECRET_KEY 是什么**:NetBox 用它加密设备密码等敏感数据。

- **全新部署(没有源数据)**:把它改成**任何 50+ 位的随机字符串**就行(下面这条命令可以生成一个):
  ```bash
  openssl rand -base64 50
  ```
  把输出粘进去。
- **以后要从源服务器恢复数据**:必须改成**源服务器** `/opt/netbox-docker/netbox.env` 里的 `SECRET_KEY=...` 那个值。**只有 SECRET_KEY 一致,恢复数据时设备密码才能被解密**。

改完保存退出(nano 里:`Ctrl+O` → `Enter` → `Ctrl+X`)。

### 第 5 步:启动

```bash
sudo docker compose -f compose.image.yml up -d
```

> **做什么**:Docker 读 `compose.image.yml`,从 ghcr.io 拉取镜像,然后启动 6 个容器:
> - `netbox` — 主服务(Web UI 在 8000 端口)
> - `netbox-worker` / `netbox-housekeeping` — 后台任务
> - `postgres` / `redis` / `redis-cache` — 数据库和缓存
>
> `up -d` = "Up + detached" = 后台运行。
>
> **验证**(应看到 6 个容器都 `Started`):
> ```bash
> sudo docker compose -f compose.image.yml ps
> ```

### 第 6 步:等 NetBox 就绪(约 1-2 分钟)

```bash
curl -sI http://127.0.0.1:8000/ | head -1
```

> **做什么**:向本机的 NetBox 发个 HTTP 请求,看它有没有启动好。
> **期望输出**:`HTTP/1.1 302 Found`
> 含义:NetBox 已就绪,看到你没登录就把你重定向到登录页。

如果 5 分钟后还是没 302,看日志查原因:
```bash
sudo docker compose -f compose.image.yml logs netbox | tail -30
```

### 第 7 步:填充图标(首次部署必须执行!)

```bash
sudo docker compose -f compose.image.yml exec netbox \
  python3 /opt/netbox/netbox/manage.py collectstatic --no-input
```

> **做什么**:NetBox 启动时**不会自动**把插件的 256 个图标复制到图标卷(已知的限制)。这条命令手动把镜像里的图标"铺"到图标卷里。
> **期望输出**:`N static files copied`(`N` 大约 300+,含 256 个图标)

### 第 8 步:验证

```bash
# 图标卷应有 57 个内置图标 + 8 个分组目录
sudo ls /opt/netbox-mzl/icons/ | head
sudo ls -d /opt/netbox-mzl/icons/*/ | head

# 所有 6 个容器都应 Up
sudo docker compose -f compose.image.yml ps
```

---

### 第 9 步:浏览器访问

打开 **`http://<服务器IP>:8000`**,登录:

- 账号:**`admin`**
- 密码:**`123456`**

(首次启动时,entrypoint 根据 `compose.image.yml` 里的 `SUPERUSER_USERNAME` / `SUPERUSER_PASSWORD` 自动创建管理员账号 `admin` / `123456`。)

进去后:
- 顶部应出现 **「拓扑」** 菜单(含「实时拓扑」「我的拓扑」)
- 「偏好设置 → 图标设置」应有 **8 个分组共 256 个华三图标** —— 部署成功

---

### 第 10 步(可选):恢复源服务器数据

要让这台新服务器和你的源服务器数据完全一致(14 台设备、线缆、坐标、角色图标绑定等):

1. 从源服务器导出数据库(参考 `docs/DEPLOY.md` 第 8.1 节)
2. 恢复到本服务器(参考同节)
3. 重启容器

**SECRET_KEY 必须与源服务器一致** —— 这就是第 4 步的意义。

---

## 常见问题

**Q: 浏览器打不开 8000 端口**
- 检查防火墙:`sudo ufw allow 8000`
- 检查容器是否都在 Up:`sudo docker compose -f compose.image.yml ps`

**Q: 图标设置是空的(没有图标)**
- 第 7 步的 `collectstatic` 没执行,再跑一次。

**Q: 想换端口(8000 → 别的)**
- 编辑 `compose.image.yml` 里 `ports: - "8000:8080"`,改左边的 `8000`。8080 别动(那是容器内部端口)。

**Q: 以后更新版本(比如 1.0.1 → 1.0.2)**
- 编辑 `compose.image.yml` 把 `image:` 末尾的 `1.0.1` 改成新版本号
- `sudo docker compose -f compose.image.yml up -d`

**Q: 出错了,怎么看日志**
```bash
sudo docker compose -f compose.image.yml logs netbox | tail -50
```

---

## 这套部署跑完,你会得到什么

- 一个跑在 `http://<服务器IP>:8000` 的 NetBox 4.6.8
- 中文界面(菜单、页面、按钮全部中文)
- 拓扑插件:实时拓扑 + 我的拓扑(已保存视图)+ 图标设置(网页上传图标、分组管理)
- **8 组共 256 个华三(H3C)设备图标** + 49 个默认图标
- 管理员账号 `admin` / `123456`
- 数据:全新空(可空库用,或按第 10 步恢复源服务器数据)
