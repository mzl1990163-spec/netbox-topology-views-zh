#!/usr/bin/env bash
# ============================================================
# 恢复 NetBox 数据库备份(用于全新部署后把数据搬过来,
# 或覆盖现有数据)
#
# 用法(在仓库根目录):
#   ./deploy/restore-db.sh <备份.sql> [netbox-docker目录]
#
# 注意:恢复前请确保 netbox.env 的 SECRET_KEY 与源服务器一致,
# 否则设备密码等加密数据无法解密。
# ============================================================
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NBD_DIR="${2:-$REPO_DIR/netbox-docker}"
DUMP="${1:?用法: ./deploy/restore-db.sh 备份.sql}"

if [ ! -f "$DUMP" ]; then
  echo "❌ 找不到备份文件: $DUMP"; exit 1
fi
cd "$NBD_DIR"

echo "==> [1/4] 停止 netbox 应用(保留 postgres)"
docker compose stop netbox netbox-worker netbox-housekeeping

echo "==> [2/4] 清空数据库 schema(保留数据库本身)"
docker compose exec -T postgres sh -c 'psql -U netbox -d netbox -c "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA IF NOT EXISTS public; ALTER SCHEMA public OWNER TO netbox;"'

echo "==> [3/4] 恢复备份: $DUMP"
docker compose exec -T postgres sh -c 'psql -U netbox -d netbox' < "$DUMP"

echo "==> [4/4] 启动 netbox(用 up -d,确保读取最新的 netbox.env)"
docker compose up -d netbox netbox-worker netbox-housekeeping

echo ""
echo "✅ 恢复完成!用源服务器的管理员账号登录即可。"
