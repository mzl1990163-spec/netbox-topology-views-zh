# ============================================================
# NetBox 额外配置:菜单 UI 美化(一级菜单底色 + 底部横线)
#
# 说明:
#   通过 NetBox 的 BANNER_TOP(页面顶部横幅)注入 CSS,
#   实现侧边栏一级菜单浅蓝底色 + 底部横线 + 子菜单样式优化。
#   内容与源服务器 14(/opt/netbox-docker/configuration/extra.py)保持一致。
#
# 部署:
#   镜像版(compose.image.yml)已挂载本文件到 /etc/netbox/config/extra.py
# ============================================================
BANNER_TOP = '''
<style>
/* ===== NetBox 菜单 UI 美化 v2 ===== */

/* 一级分组标题:浅蓝底色 + 加粗 + 品牌色 + 底部横线分隔 */
#sidebar-menu .nav-item.dropdown > .nav-link {
  font-weight: 600;
  color: #0b5fa8 !important;
  background: #e6f0fa;
  border-bottom: 1px solid #c9d9ea;
  border-radius: 4px;
  padding-top: 8px;
  padding-bottom: 8px;
}
#sidebar-menu .nav-item.dropdown > .nav-link .nav-link-title {
  font-size: 0.92rem;
}

/* 一级分组 hover 加深底色 */
#sidebar-menu .nav-item.dropdown > .nav-link:hover {
  background: #d6e7f7;
  border-bottom-color: #0b5fa8;
}

/* 子菜单:统一缩进 + 左侧色条,层级分明 */
#sidebar-menu .dropdown-menu .dropdown-item {
  padding-left: 34px !important;
  border-left: 3px solid transparent;
  margin: 1px 6px;
  border-radius: 4px;
  font-size: 0.9rem;
}

/* 子菜单 hover 反馈 */
#sidebar-menu .dropdown-menu .dropdown-item:hover {
  background: #eef3fa;
  border-left-color: #8ab8e8;
}

/* 当前激活项:色条 + 浅色背景 + 加粗 */
#sidebar-menu .dropdown-menu .dropdown-item.active {
  background: rgba(11, 95, 168, 0.10);
  border-left-color: #0b5fa8;
  color: #0b5fa8;
  font-weight: 600;
}

/* 子菜单图标微调 */
#sidebar-menu .dropdown-menu .dropdown-item .dropdown-item-icon {
  color: #0b5fa8;
  opacity: 0.75;
}
</style>
'''
