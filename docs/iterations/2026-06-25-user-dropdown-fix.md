# 2026-06-25 用户头像下拉菜单修复

## 问题

平台右上角用户头像按钮点击后，`core.js` 已经给菜单添加展开状态，但下拉菜单内容不可见。

## 原因

`.user-dropdown__menu` 使用绝对定位展示在头像按钮下方；其祖先 `.header-right` 设置了 `overflow-x: auto`。浏览器会将另一个轴向的 overflow 计算为可裁剪滚动容器，导致菜单即使进入展开状态也被父容器裁掉。

## 修改

- 将 `.header-right` 从横向滚动容器调整为 `overflow: visible`，允许头像下拉菜单向下溢出显示。
- 给 `.header-right` 和 `.site-nav` 增加 flex 收缩约束，保留导航链接自身的横向滚动能力。
- 增加回归测试，验证登录态 header 渲染通知菜单入口，并验证 `.header-right` 不再使用会裁剪下拉菜单的 `overflow-x: auto`。

## 验证

- 通过：`uv run pytest tests/test_platform_foundation.py -q`，4 passed。
- 通过：`uv run --no-sync ruff check apps base_framework celery_app tests manage.py`。
- 通过：`uv run --no-sync mdformat --check docs/iterations/2026-06-25-user-dropdown-fix.md`。
- 未通过：`uv run --no-sync ruff format --check apps base_framework celery_app tests manage.py`，现有 `base_framework/settings/base.py` 需要格式化；本次未纳入无关换行改动。
- 未通过：`make test`，2 个既有首页文案断言仍期待 `让每一个`，当前首页实际文案已变更；本次头像下拉菜单修复的聚焦测试通过。
