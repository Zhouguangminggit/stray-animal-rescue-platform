# 第 1 批（UI 基础设计系统）：暖橙主题全局重构

## 实施内容

### 设计系统
- **重构 `static/css/foundation.css`**：从深绿色暗黑主题全面替换为暖橙主题（`#FF8C42`）。定义了完整的设计令牌：品牌色、中性色、背景色、功能色、阴影、字体栈（Manrope + ZCOOL XiaoWei）、圆角、间距、过渡。全局样式从 `color-scheme: dark` 改为 `color-scheme: light`。

### 组件库（新建）
- **`static/css/components/typography.css`**：Eyebrow 标签、显示标题（display-heading）、正文层级、文字颜色/对齐/字重工具类、链接样式。
- **`static/css/components/buttons.css`**：基础按钮 `.btn`、次要按钮 `.btn--secondary`、幽灵按钮 `.btn--ghost`、宽/小/大/图标/链接/禁用等变体，含悬停动画和箭头位移效果。
- **`static/css/components/cards.css`**：基础卡片 `.card`、服务卡片 `.service-card`、统计卡片 `.stat-card`、参与行动卡片 `.involve-card`、动物卡片 `.pet-card`，含悬停上浮和阴影增强。
- **`static/css/components/forms.css`**：输入框、文本域、选择框、复选框/单选框、内联字段、帮助文本、错误列表、搜索框、验证码按钮等表单元素，聚焦状态使用暖橙 ring。

### 全局布局与外壳
- **重构 `templates/layouts/application.html`**：更新 `theme-color` 为 `#FF8C42`，加载 Google Fonts（Manrope + ZCOOL XiaoWei），引入全部组件 CSS，保留所有 `{% block %}` 结构。
- **重构 `templates/components/site_header.html`**：移除硬编码的 "stray-animal-rescue-platform" 品牌文案，保留完整的导航逻辑（登录/未登录状态、管理员入口、通知、我的救助/领养、退出）。
- **重构 `static/css/components/site-shell.css`**：头部导航改为暖白毛玻璃背景（`rgba(255, 248, 240, 0.92)`），滚动后增强阴影和边框色；导航链接悬停改为 `--primary` 橙色；主按钮（`.site-nav__primary`）改为实心橙；用户头像渐变改为暖橙；消息提示改为暖色系（成功/错误/警告/信息四种变体）；FAQ 模块边框和颜色统一为暖色；保留完整移动端适配。
- **重构 `static/js/core.js`**：保留消息提示自动关闭逻辑；新增导航栏滚动监听（`requestAnimationFrame` 优化），滚动超过 16px 后添加 `site-header--scrolled` 类；新增锚点链接平滑滚动。

### 认证模块（最小兼容更新，避免崩坏）
- **重构 `static/accounts/css/auth.css`**：将所有旧 CSS 变量（`--brand-olive`、`--brand-brown` 等）替换为新暖橙变量；左侧视觉栏渐变改为暖橙色调；右侧表单面板改为暖白背景；输入框聚焦改为暖橙 ring；按钮改为圆角药丸形实心橙；保留原有布局结构（双栏/响应式）。
- **重构 `static/accounts/css/profile.css`**：替换所有旧变量为暖橙变量；深绿色半透明背景改为白色卡片；边框和装饰色改为暖橙；头像渐变改为暖橙；保存按钮渐变改为暖橙；保留原有双栏布局。
- **更新 `templates/accounts/auth_base.html`**：将硬编码的 "stray-animal-rescue-platform" 品牌文案替换为 `{{ site_name }}` 变量，视觉栏文案改为平台使命描述。
- **更新 `templates/accounts/media.html`**：移除 alt 中的 "stray-animal-rescue-platform"。
- **更新 `templates/accounts/register.html`**：将 "加入 stray-animal-rescue-platform" 改为 "加入我们"。

### 验证结果
- 代码检查：无 CSS/HTML 文件使用已移除的旧变量（`--brand-brown`、`--brand-olive` 等）。
- 品牌文案：除 `README.md`、`README.en.md`、`skill/SKILL.md`（第十一批处理）和本项目文档外，模板中已无 "stray-animal-rescue-platform" 硬编码文案。
- 未修改业务逻辑：所有模板 `{% block %}`、`{% url %}`、表单字段、权限判断、消息提示等逻辑完全保留。

## 待后续批次处理

- 首页（`core/home.html` + `home.css`）：第二批重点重构，需实现 home-style 全部区块（Hero、关于我们、服务、动物卡片、参与行动、数据统计、联系我们、页脚）。
- 认证页面视觉优化：auth.css 当前为最小兼容版本，左侧栏渐变和右侧面板样式可进一步提升为与 home-style 一致的现代感。
- 各业务模块 CSS（`animals.css`、`adoptions.css`、`community.css` 等）：仍使用硬编码绿色值，后续批次逐步替换为暖橙变量。
- `README.md` / `README.en.md` / `skill/SKILL.md`：品牌文案清理在第十一批完成。
