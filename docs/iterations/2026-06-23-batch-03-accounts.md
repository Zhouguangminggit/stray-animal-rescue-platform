# 第 3 批（认证模块）：暖橙风格统一

## 实施内容

### 1. 认证视觉资源更新
- **更新 `base_framework/settings/base.py`**：将 `AUTH_MEDIA` 的默认路径从旧 `accounts/media/djangoharness.png` 改为暖橙主题图片：
  - login → `core/img/hero-bg.jpg`
  - register → `core/img/about-volunteer.jpg`
  - password_reset → `core/img/hero-bg.jpg`

### 2. 认证 CSS 增强（`static/accounts/css/auth.css`）
在第一批已完成的暖橙兼容基础上，新增：
- **`.auth-panel .eyebrow`**：覆盖全局 `typography.css` 的药丸背景样式，使认证页面的 eyebrow 恢复为简洁文字标签（无背景、无 padding），避免与暖橙药丸背景冲突
- **`.auth-success`**：成功状态卡片（居中、图标、标题、描述），用于密码重置完成/邮件发送等状态页
- **`.auth-form-wrap .card`**：认证面板内的通用卡片样式（白色背景、阴影、圆角），确保 `password_reset_done.html` 的卡片正确显示

### 3. 模板修复与优化

#### `password_reset_done.html`（关键修复）
- **原问题**：使用 `{% block content %}` 覆盖了 `auth_base.html` 的整个 `content` 块，导致左侧视觉面板和右侧认证面板完全消失，只显示一个孤立卡片
- **修复**：改为 `{% block auth_content %}`，使内容正确嵌入认证面板的 `auth-form-wrap` 中
- **样式升级**：使用新的 `.auth-success` 成功卡片样式（大图标 + 标题 + 描述）

#### `password_reset_complete.html`
- **样式升级**：同样使用 `.auth-success` 成功卡片样式，统一密码重置流程的视觉体验

### 4. 已保留未改动的模板（第一批已兼容）
- `auth_base.html`：双栏布局（左视觉 + 右表单）已适配暖橙主题
- `login.html`：登录表单完整保留 CSRF、next 跳转、表单字段、忘记密码链接
- `register.html`：注册表单完整保留账号/手机 Tab 切换、mode 隐藏字段
- `password_reset_form.html`：找回密码表单完整保留
- `password_reset_confirm.html`：设置新密码表单完整保留
- `profile.html`：个人资料页面使用第一批已更新的 `profile.css`，保持双栏布局（左摘要 + 右编辑）
- `form_fields.html`：表单字段渲染逻辑完全保留

## 验证结果
- CSS 括号平衡：通过
- 模板标签配对：所有认证模板 `{% block %}` / `{% endblock %}` 正确匹配
- 品牌文案检查：无模板包含 "DjangoHarness"
- URL 引用检查：所有 `{% url %}` 引用均为有效命名路由
- 功能保留：登录、注册、密码重置、个人资料编辑的所有业务逻辑未改动

## 待后续批次处理
- 联系表单后端提交（当前首页联系表单仅前端展示）
- 动画升级：认证页面可进一步添加 Framer Motion 级别的入场动画
