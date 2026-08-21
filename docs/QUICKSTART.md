# 快速部署指南(镜像版 v1.0.1)

> 在一台新服务器上,用镜像部署 NetBox 4.6.8 + 拓扑插件 + 256 图标。
> 按顺序一条一条执行即可,总耗时约 5 分钟(含首次启动 2 分钟)。

## 0. 准备

- 一台 Ubuntu 22.04 / 24.04 服务器(有 root 或 sudo)
- 能访问 GitHub 和 ghcr.io(镜像公开,免登录)

---

## 1. 安装 Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
```

## 2. 创建部署目录

```bash
sudo mkdir -p /opt/netbox-mzl/configuration
cd /opt/netbox-mzl
```

## 3. 获取部署文件

```bash
# 下载 compose 文件(来自 GitHub 仓库)
sudo wget -O compose.image.yml \
  https://raw.githubusercontent.com/mzl1990163-spec/netbox-topology-views-zh/main/deploy/compose.image.yml

# 创建插件启用配置
echo 'PLUGINS = ["netbox_topology_views"]' | sudo tee configuration/plugins.py
```

## 4. 修改 SECRET_KEY(必须与源服务器一致)

```bash
sudo nano compose.image.yml
```

找到这一行,把值改成**源服务器(数据来源)的 SECRET_KEY**:

```yaml
SECRET_KEY: "改成与源服务器一致的SECRET_KEY"
```

> 只有 SECRET_KEY 一致,以后恢复数据时设备密码才能解密。保存退出。

## 5. 启动

```bash
sudo docker compose -f compose.image.yml up -d
```

## 6. 等待就绪(约 1-2 分钟)

```bash
curl -sI http://127.0.0.1:8000/ | head -1
```

期望输出:`HTTP/1.1 302 Found`(说明 NetBox 已启动,跳到登录页)。

## 7. 填充图标(重要,首次部署必做)

```bash
sudo docker compose -f compose.image.yml exec netbox \
  python3 /opt/netbox/netbox/manage.py collectstatic --no-input
```

输出应包含:`N static files copied`(约 300+ 个,含 256 图标)。

## 8. 验证

```bash
# 所有容器都应 Up
sudo docker compose -f compose.image.yml ps

# 图标目录应有 57+ 个内置图标和 8 个分组
ls /opt/netbox-mzl/icons/
```

## 9. 浏览器访问

```
http://服务器IP:8000
```

登录账号:`admin` / `123456`(首次启动自动创建)。

## 10. (可选)恢复源服务器数据

需要和源服务器数据一致时,按 [docs/DEPLOY.md](DEPLOY.md) 第 8.1 节操作(pg_dump / restore-db.sh)。
