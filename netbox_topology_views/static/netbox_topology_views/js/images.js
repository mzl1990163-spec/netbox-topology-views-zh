(() => {
  // ---------- Toast ----------
  const toast = (cls, msg) => {
    const t = document.querySelector(cls);
    if (!t) return console.error("toast not found:", cls);
    t.querySelector("span").textContent = msg;
    new window.Toast(t).show();
  };
  const toastSuccess = (m) => toast("#topology-plugin-success-toast", m);
  const toastError = (m) => toast("#topology-plugin-error-toast", m);

  // 当前选择: role_id -> image url
  const selections = {};

  // ---------- 图标网格渲染 ----------
  function renderGroup(roleId, groupName) {
    const menu = document.querySelector(`.role-image-menu[data-role="${roleId}"]`);
    if (!menu) return;
    // 注意: IMAGE_GROUPS/ROLE_IMAGES 是 <script> 顶层 const(全局词法环境),不在 window 上
    const icons = (IMAGE_GROUPS && IMAGE_GROUPS[groupName]) || [];
    const current = (ROLE_IMAGES && ROLE_IMAGES[roleId]) || "";
    menu.innerHTML = "";
    if (!icons.length) {
      menu.innerHTML = '<div class="p-3 text-muted">该分组暂无图标</div>';
      return;
    }
    const grid = document.createElement("div");
    grid.className = "icon-grid";
    icons.forEach((icon) => {
      const img = document.createElement("img");
      img.src = icon.url;
      img.title = icon.name;
      img.alt = icon.name;
      img.dataset.role = roleId;
      img.dataset.image = icon.url;
      if (icon.url === current) img.classList.add("selected");
      grid.appendChild(img);
    });
    menu.appendChild(grid);
  }

  // ---------- 上传区:新建分组(浏览器原生 prompt + 立即创建) ----------
  const uploadGroup = document.querySelector("#upload-group");
  if (uploadGroup) {
    uploadGroup.addEventListener("change", () => {
      if (uploadGroup.value !== "__new__") return;
      // 恢复默认,避免卡在"新建分组"选项
      uploadGroup.value = "内置";
      const raw = window.prompt("请输入新分组名(仅字母/数字/-_,如 h3c-server):");
      if (raw === null) return; // 用户取消
      const name = raw.trim();
      if (!name) {
        toastError("分组名不能为空");
        return;
      }
      if (!/^[A-Za-z0-9_-]+$/.test(name)) {
        toastError("分组名仅允许字母/数字/-_");
        return;
      }
      // 立即请求后端创建分组目录
      fetch(`/${basePath}plugins/netbox_topology_views/images/create-group/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": window.CSRF_TOKEN,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `group=${encodeURIComponent(name)}`,
      })
        .then((res) => res.json().catch(() => ({ error: "响应解析失败" })))
        .then((data) => {
          if (!data.ok) {
            toastError(data.error || "创建分组失败");
            return;
          }
          // 已存在则直接选中,否则加入下拉
          let opt = Array.from(uploadGroup.options).find((o) => o.value === name);
          if (!opt) {
            opt = new Option(name, name, true, true);
            uploadGroup.appendChild(opt);
          }
          uploadGroup.value = name;
          toastSuccess(`分组 "${name}" 已创建,点上传将图标传进该组`);
        })
        .catch((err) => {
          console.dir(err);
          toastError("创建分组失败,请重试");
        });
    });
  }

  // ---------- 上传区:分组下拉与角色列表等宽(不写死像素,随窗口自适应) ----------
  function syncUploadGroupWidth() {
    const firstRoleSelect = document.querySelector(".role-group-select");
    if (firstRoleSelect && uploadGroup) {
      uploadGroup.style.width = firstRoleSelect.offsetWidth + "px";
    }
  }
  syncUploadGroupWidth();
  window.addEventListener("resize", syncUploadGroupWidth);

  // ---------- 列表:分组下拉 -> 渲染对应分组图标 ----------
  document.querySelectorAll(".role-group-select").forEach((sel) => {
    sel.addEventListener("change", () => renderGroup(sel.dataset.role, sel.value));
    renderGroup(sel.dataset.role, sel.value);
  });

  // ---------- 图标点击:选中并更新按钮 ----------
  document.querySelectorAll(".role-image-menu").forEach((menu) => {
    menu.addEventListener("click", (e) => {
      if (!(e.target instanceof HTMLImageElement)) return;
      const roleId = e.target.dataset.role;
      const imageUrl = e.target.dataset.image;
      if (!roleId || !imageUrl) return;
      selections[roleId] = imageUrl;
      const btn = document.querySelector(`.role-image-btn[data-role="${roleId}"]`);
      if (btn) btn.innerHTML = `<img src="${imageUrl}" alt="图标">`;
      menu.querySelectorAll("img").forEach((i) => i.classList.toggle("selected", i === e.target));
    });
  });

  // ---------- 保存 ----------
  const imagesForm = document.querySelector("form#images");
  if (imagesForm) {
    imagesForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        const res = await fetch(`/${basePath}api/plugins/netbox_topology_views/images/save/`, {
          method: "POST",
          body: JSON.stringify(selections),
          headers: {
            "X-CSRFToken": window.CSRF_TOKEN,
            "Content-Type": "application/json",
          },
        });
        if (!res.ok) throw new Error(await res.text());
        toastSuccess("设置已保存");
      } catch (err) {
        console.dir(err);
        toastError(err.message);
      }
    });
  }
})();
