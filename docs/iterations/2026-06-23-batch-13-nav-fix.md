# 第 13 批（导航栏修复 + 首页滚动优化）

## 修复问题

### 1. 导航栏下拉菜单点击无效

**原因分析**：`user-dropdown` 位于 `site-nav` 内部，而 `site-nav` 有 `overflow-x: auto`。在某些浏览器中，`overflow-x: auto` 可能会隐式设置 `overflow-y: hidden`，从而裁剪 `position: absolute` 的下拉菜单。

**修复措施**：
- 将 `user-dropdown` 移出 `site-nav`，放入独立的 `.header-right` 容器中
- 添加 `.header-right` 的 flex 布局样式
- 添加 `.auth-links` 的样式（未登录状态）
- 给 `user-dropdown__menu` 添加 `pointer-events: none`（关闭时）和 `pointer-events: auto`（展开时），防止隐藏的菜单阻挡点击
- 修改 `core.js`：使用 `document.addEventListener("click", (e) => { if (!dropdown.contains(e.target)) closeMenu(); })` 替代全局 click 监听器，避免 `stopPropagation()` 导致的问题
- 在 toggle 的 click 事件中添加 `e.preventDefault()`，确保按钮默认行为被阻止

### 2. 首页滚动到"寻找家人"模块无法继续向下滑动

**原因分析**：`pets-scroll-container` 的 `scroll-snap-type: x mandatory` 在某些浏览器（特别是移动端）中会强制捕获滚动事件，阻止垂直滚动继续。同时，动物图片文件过大可能导致加载卡顿。

**修复措施**：
- 将 `scroll-snap-type: x mandatory` 改为 `scroll-snap-type: x proximity`（更宽松的捕捉模式）
- 添加 `overscroll-behavior-x: contain` 防止水平滚动溢出影响垂直滚动
- 添加 `touch-action: pan-x pan-y` 允许水平和垂直滚动
- 给 `home.html` 中的动物图片添加 `loading="lazy" decoding="async"` 属性，减少初始加载负担

## 修改文件

| 文件 | 修改内容 |
|------|----------|
| `templates/components/site_header.html` | 将 `user-dropdown` 移出 `site-nav`，放入 `.header-right` |
| `static/css/components/site-shell.css` | 添加 `.header-right`、`.auth-links` 样式；修复 `pointer-events`；移除 `.site-nav .site-nav__user` |
| `static/js/core.js` | 修复下拉菜单事件绑定逻辑 |
| `apps/core/templates/core/home.html` | 动物图片添加 `loading="lazy" decoding="async"` |
| `static/core/css/home.css` | `scroll-snap-type: proximity` + `overscroll-behavior-x: contain` + `touch-action` |
