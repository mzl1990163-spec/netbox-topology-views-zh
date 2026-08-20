#!/usr/bin/env bash
# ============================================================
# 一键部署:在全新服务器上构建并启动与源服务器相同的
# NetBox 4.6.8 + netbox_topology_views(中文版) 环境
#
# 用法(在仓库根目录):
#   ./deploy/deploy.sh [netbox-docker目录,默认 ./netbox-docker]
#
# 部署后与源服务器"一模一样"还差两步,见部署文档:
#   1. netbox.env 的 SECRET_KEY 与源服务器一致(解密设备密码)
#   2. 恢复数据库数据(可选,deploy/restore-db.sh)
# ============================================================
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NBD_DIR="${1:-$REPO_DIR/netbox-docker}"

echo "==> [1/5] 获取 netbox-docker"
if [ ! -d "$NBD_DIR/.git" ]; then
  git clone --depth 1 https://github.com/netbox-community/netbox-docker.git "$NBD_DIR"
fi
cd "$NBD_DIR"

echo "==> [2/5] 放置插件源码到 plugin-src/"
mkdir -p plugin-src
rm -rf plugin-src/netbox_topology_views
cp -r "$REPO_DIR/netbox_topology_views" plugin-src/

echo "==> [3/5] 复制自定义构建/编排配置"
cp -f "$REPO_DIR/deploy/Dockerfile-Plugins" .
cp -f "$REPO_DIR/deploy/docker-compose.override.yml" .

echo "==> [4/5] 准备 netbox.env"
if [ ! -f netbox.env ]; then
  cp -f configuration/netbox.env.example netbox.env
  echo "   已从模板生成 netbox.env"
  echo "   ⚠️ 重要:编辑 netbox.env,把 SECRET_KEY 设为与源服务器一致"
  echo "     (否则已保存的设备密码无法解密)"
fi

echo "==> [5/5] 构建并启动"
docker compose build netbox
docker compose up -d netbox

echo ""
echo "✅ 部署完成!"
echo "   访问 http://<本机IP>:8000"
echo "   若图标未出现,执行: docker compose exec netbox python3 manage.py collectstatic --no-input"
echo "   恢复数据: 参考 deploy/restore-db.sh"
