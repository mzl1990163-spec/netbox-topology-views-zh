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

## 安装部署

### 方式一:镜像部署(推荐,一步到位)

镜像 `ghcr.io/mzl1990163-spec/netbox-topology-views-zh:1.0.1` 已内置 NetBox 4.6.8 + 插件 + 256 图标,并已启用插件。

> **第一次接触本项目?** 强烈建议先看 **[docs/QUICKSTART.md](docs/QUICKSTART.md)**,里面详细解释每个文件从哪来、每条命令做什么、为什么这么做,适合零基础照着敲。

**完整命令版教程见 [docs/QUICKSTART.md](docs/QUICKSTART.md)**。步骤概要:

1. 新建目录,把仓库里的 **`deploy/compose.image.yml`** 复制进去(已包含 netbox / postgres / redis 全部服务和环境变量);
2. 编辑 `compose.image.yml`,把 **`SECRET_KEY`** 改成与源服务器一致(否则设备密码无法解密);
3. 启动:

```bash
docker compose -f compose.image.yml up -d
```

4. 等 1~2 分钟(首次自动建库、迁移),**再执行一次 collectstatic 填充图标**:

```bash
docker compose -f compose.image.yml exec netbox python3 /opt/netbox/netbox/manage.py collectstatic --no-input
```

5. 访问 `http://<服务器IP>:8000` 即可(登录 admin / 123456)。

> 镜像公开、免登录;上传的图标自动持久化到 `./icons` 卷;更新版本只需改 `image:` 的 tag 再 `up -d`。

### 方式二:源码部署(自行构建,备选)

适合想自己构建镜像的场景,详细步骤见 [docs/DEPLOY.md](docs/DEPLOY.md)。仓库 `deploy/` 已提供现成文件:

- `deploy.sh` — 一键脚本(克隆 netbox-docker → 放插件 → 构建 → 启动)
- `Dockerfile-Plugins` — 锁定基础镜像 `ghcr.io/netbox-community/netbox:v4.6.8-5.0.2`
- `docker-compose.override.yml` — icons 持久卷挂载

首次部署后若图标未自动填充,手动执行:

```bash
sudo docker exec <netbox容器名> python3 manage.py collectstatic --no-input
```

## 常见问题

- **拓扑只显示连线不显示设备**:多为图标 404 或设备无坐标。检查 `img` 目录是否存在图标、`collectstatic` 是否执行,并给设备补充坐标。
- **新建分组刷新后看不到**:本版已修复(空分组也会列出)。上传图标后即可在分组中看到。
- **改了代码不生效**:`plugin-src` 在构建镜像时打进镜像,**必须重新 `docker compose build netbox` 并 `up -d`**,仅重启容器不会生效。
- **图标命名**:建议 `分组名-NN`(如 `Switch-01`),序号连续、易管理。

## License

- 插件本体:Apache-2.0(保留上游版权)。
- 内置默认图标集:CC BY-SA 4.0(见 `netbox_topology_views/static/netbox_topology_views/img/LICENSE`)。
- 华三(H3C)设备图标版权归新华三集团所有,仅限内部使用,请勿公开分发。

## 致谢

- 上游项目:[netbox-topology-views](https://github.com/mattieserver/netbox-topology-views)(作者 Mattijs Vanhaverbeke,Apache-2.0)
- [netbox-docker](https://github.com/netbox-community/netbox-docker) 部署方案
