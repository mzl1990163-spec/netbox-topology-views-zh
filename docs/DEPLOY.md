# 部署文档(netbox-docker)

本插件通过 netbox-docker 部署,源码放在 `plugin-src/` 下,构建镜像时打入容器。

## 0. 环境

- netbox-docker(基于 `ghcr.io/netbox-community/netbox:v4.6.8-5.0.2`,与源服务器一致)
- Docker / Docker Compose v2
- 已验证:NetBox 4.6.8、netbox-docker 5.0.2

> 仓库 `deploy/` 目录已包含现成的部署文件:`Dockerfile-Plugins`(锁版本)、`docker-compose.override.yml`、一键脚本 `deploy.sh`。推荐直接用:
>
> ```bash
> cd 仓库根目录
> ./deploy/deploy.sh
> ```
>
> 以下为手动步骤说明。

## 1. 放置插件源码

把本仓库的 `netbox_topology_views/` 目录放到 netbox-docker 的 `plugin-src/` 下:

```bash
# 在 netbox-docker 目录内
mkdir -p plugin-src
cp -r netbox_topology_views plugin-src/
```

## 2. Dockerfile-Plugins(构建插件镜像)

在 netbox-docker 根目录创建 `Dockerfile-Plugins`:

```dockerfile
FROM ghcr.io/netbox-community/netbox:latest

# 插件源码
COPY plugin-src/ /opt/netbox_topology_views/

# 直接把插件的 JS/CSS/图标 COPY 到 NetBox 静态目录(避免 collectstatic 权限问题)
COPY plugin-src/netbox_topology_views/static/netbox_topology_views/ /opt/netbox/netbox/static/netbox_topology_views/

# 创建图标目录并安装插件
RUN mkdir -p /opt/netbox/netbox/static/netbox_topology_views/img && \
    uv pip install --python /opt/netbox/venv/bin/python3 --no-cache /opt/netbox_topology_views && \
    rm -rf /opt/netbox_topology_views
```

## 3. docker-compose.override.yml(挂载图标持久卷)

**关键**:把 `/icons` 目录挂载到插件的图标目录,这样网页上传的图标和自定义分组在重建容器后不会丢失。

```yaml
services:
  netbox: &netbox
    build:
      context: .
      dockerfile: Dockerfile-Plugins
    ports:
      - "8000:8080"   # 按需修改端口
    volumes:
      - ./icons:/opt/netbox/netbox/static/netbox_topology_views/img

  netbox-worker:
    <<: *netbox
    ports: []

  netbox-housekeeping:
    <<: *netbox
    ports: []
```

> 该 override 同时作用于 `netbox`、`netbox-worker`、`netbox-housekeeping` 三个服务。

## 4. 启用插件(configuration.py)

在 NetBox 的 `configuration.py` 中加入:

```python
PLUGINS = ["netbox_topology_views"]
```

## 5. 构建并启动

```bash
cd /opt/netbox-docker
docker compose build netbox
docker compose up -d netbox
```

> 提示:插件源码是**构建时**打进镜像的。之后任何代码改动都需要重新执行上面两条命令,仅 `docker compose restart` 不会生效。

## 6. 首次部署:初始化图标

netbox-docker 启动时通常会自动执行 `collectstatic`,把镜像内图标写入挂载卷。若 `/icons` 卷为空、页面上看不到任何图标,手动执行一次:

```bash
sudo docker exec netbox-docker-netbox-1 python3 manage.py collectstatic --no-input
```

之后即可在「网络拓扑 → 偏好设置 → 图标设置」页面看到 8 个分组共 256 个华三图标 + 49 个内置图标。

## 7. 使用与验证

1. 顶部导航出现「拓扑」菜单(含「实时拓扑」「我的拓扑」);
2. 「偏好设置 → 图标设置」:上传图标、新建分组、为每个设备角色选择图标并保存;
3. 「实时拓扑」页:拓扑图按角色显示对应图标,支持过滤与导出;
4. 「我的拓扑」:保存当前视图,之后一键回到。

## 8. 升级插件

```bash
# 用新版本源码替换 plugin-src/netbox_topology_views/
cd /opt/netbox-docker
docker compose build netbox
docker compose up -d netbox
```

图标卷 `./icons` 不受重建影响,已上传的图标与分组都会保留。

## 8.1 数据迁移(让新服务器和旧服务器数据一模一样)

插件/图标只包含"功能";设备、线缆、坐标、角色图标绑定、已保存视图等**数据在数据库里**,要整体迁移需要导出/恢复数据库。

**第一步:在旧服务器导出**

```bash
cd /opt/netbox-docker
docker compose exec postgres sh -c 'pg_dump -U netbox -d netbox' > netbox-dump.sql
```

**第二步:在新服务器恢复(推荐用脚本)**

仓库已提供 `deploy/restore-db.sh`,会自动停应用 → 清空 schema → 恢复 → 启动:

```bash
cd 仓库根目录
./deploy/restore-db.sh /path/to/netbox-dump.sql
```

**关键:SECRET_KEY 必须一致**

NetBox 用 `SECRET_KEY` 加密设备密码等敏感数据。新服务器的 `netbox.env` 里把 `SECRET_KEY` 设为与旧服务器**完全相同**的值,否则恢复后设备密码无法解密(显示为密文)。不要把这个值写进 git。

> 注:导出文件里含设备密码等敏感数据(加密存储),请妥善保管,不要放入公开仓库。
>
> 手动恢复(不依赖脚本):
> ```bash
> docker compose stop netbox netbox-worker netbox-housekeeping
> docker compose exec -T postgres sh -c 'psql -U netbox -d netbox -c "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA IF NOT EXISTS public;"'
> docker compose exec -T postgres sh -c 'psql -U netbox -d netbox' < netbox-dump.sql
> docker compose up -d netbox netbox-worker netbox-housekeeping   # 用 up -d 而非 start,确保读取最新 netbox.env
> ```

## 9. 排错速查

| 现象 | 处理 |
| --- | --- |
| 拓扑只有连线没有设备图标 | 检查 `img` 目录是否存在;执行 collectstatic;给设备补充坐标 |
| 上传图标后刷新不显示 | 检查 `/icons` 卷写入权限;确认文件名不含中文/特殊字符 |
| 新建分组刷新后消失 | 确认插件为最新版(空分组也会列出);查看容器日志 |
| 修改代码后无变化 | 必须 `docker compose build netbox` 重建(代码在构建时打入镜像) |
| 图标目录权限错误 | `sudo chmod -R 777 /opt/netbox-docker/icons`(容器内 netbox 用户 uid 999) |
