# 流浪动物救助平台 — UI 重构分批次完善计划

> 基于 `home-style` 首页暖橙风格（#FF8C42），在保证所有业务功能不变的前提下，逐批重构 Django 模板的 HTML/CSS/JS。

---

## 已掌握的项目现状

### 后端模块（8 个 apps）
| 模块 | 功能页面 | 模板文件 |
|------|----------|----------|
| `core` | 首页、健康检查 | `core/home.html` |
| `accounts` | 登录、注册、忘记密码、重置密码、个人资料 | `auth_base.html`, `login.html`, `register.html`, `password_reset_*.html`, `profile.html` |
| `animals` | 动物列表、详情、救助申请、我的救助 | `list.html`, `detail.html`, `rescue_form.html`, `my_rescues.html` |
| `adoptions` | 领养列表、详情、申请、我的领养 | `list.html`, `detail.html`, `apply_form.html`, `mine.html` |
| `activities` | 活动列表、详情、报名、取消 | `list.html`, `detail.html` |
| `donations` | 捐赠项目列表、详情、认捐 | `list.html`, `detail.html` |
| `volunteers` | 社区列表、文章详情、帖子、志愿者申请 | `community_list.html`, `article_detail.html`, `post_detail.html`, `apply_form.html` |
| `notifications` | 通知列表、详情 | `list.html`, `detail.html` |

### 全局基础
- `templates/layouts/application.html` — 基础布局（需全局重构）
- `templates/components/site_header.html` — 站点头部导航
- `templates/components/messages.html` — Django messages 提示
- `templates/components/faq_section.html` — FAQ 组件
- `static/css/foundation.css` — 当前为深绿色暗黑主题，需整体替换为暖橙风格
- `static/css/components/site-shell.css` — 站点外壳样式
- `static/js/core.js` — 全局交互脚本

### `home-style` 风格关键要素（需迁移到 Django）
- **主色**：`#FF8C42`（橙）、`#2D2A26`（深棕）、`#FFF8F0`（暖白）
- **字体**：Manrope、ZCOOL XiaoWei（展示标题）
- **设计元素**：圆角卡片、毛玻璃导航、渐变文字、悬停放大、计数动画、滚动揭示
- **首页区块**：Hero → 关于我们 → 服务 → 动物卡片 → 参与行动 → 数据统计 → 联系我们 → 页脚

---

## 分批次完善计划（共 11 批）

### 第一批：基础设计系统 + 全局布局（高优先级，所有后续批次的前置）

**目标**：建立统一的 CSS 变量、组件样式和页面骨架，确保所有页面共用一套设计语言。

**具体工作**：
1. **重构 `static/css/foundation.css`**
   - 替换全部 CSS 变量为暖橙主题：`--primary: #FF8C42`, `--dark: #2D2A26`, `--warm-white: #FFF8F0`, `--light-orange: #FFF0E0`
   - 引入新字体栈（Manrope + ZCOOL XiaoWei + 系统回退）
   - 定义全局文字、间距、圆角、阴影标准
2. **重构 `templates/layouts/application.html`**
   - 更新 `<meta theme-color>`、加载新字体 CDN
   - 保留 `{% block %}` 结构，确保各模块模板继承正常
3. **重构 `templates/components/site_header.html`**
   - 保留现有导航链接逻辑，但样式改为 `home-style` 导航风格（透明背景 → 滚动后毛玻璃）
   - 保留用户登录/未登录状态切换
   - 保留品牌 Logo 占位，后续替换为 Street Pet Society 品牌图
4. **创建 `static/css/components/` 通用组件库**
   - `buttons.css`：主按钮（实心橙）、次要按钮（边框橙）、幽灵按钮
   - `cards.css`：圆角卡片、阴影、悬停效果
   - `forms.css`：输入框、选择框、文本域的暖橙聚焦样式
   - `typography.css`：eyebrow 标签、GradientText 渐变标题、正文层级
5. **重构 `static/js/core.js`**
   - 添加导航栏滚动监听（切换毛玻璃背景）
   - 保留现有的消息提示自动关闭逻辑

**验收标准**：
- 任意页面打开后，导航栏、基础字体、按钮、表单都呈现暖橙风格
- 所有现有页面无样式崩坏

---

### 第二批：首页（core/home.html）— 最高优先级

**目标**：与 `home-style` 首页 100% 风格一致，包含所有视觉区块。

**具体工作**：
1. **Hero 区域**
   - 全屏背景图（需将 `home-style/public/images/hero-bg.jpg` 等资源复制到 `static/core/img/`）
   - 大标题“给流浪动物一个温暖的家”+ eyebrow“关爱每一个小生命”
   - CTA 按钮：“领养一只宠物”、“了解我们的使命”
2. **关于我们（AboutSection）**
   - 左文右图布局，展示平台介绍和统计数据（3,000+ / 80% / 200+）
   - 图片需使用 `about-volunteer.jpg`
3. **我们的服务（ServicesSection）**
   - 6 卡片网格：动物救助、医疗救助、领养服务、社区教育、志愿者招募、绝育计划
   - 每个卡片含图标、标题、描述
4. **等待回家的小伙伴们（PetsSection）**
   - 水平滚动/轮播展示最新可领养动物（调用 `latest_animals` 数据）
   - 卡片含动物照片、名字、品种、年龄、性格描述
5. **你可以怎样帮忙（GetInvolvedSection）**
   - 3 张大图卡片：领养一只宠物、捐赠支持、成为志愿者
6. **数据统计（StatsSection）**
   - 4 个数字计数动画：已救助动物、成功领养、医疗服务、活跃志愿者
7. **联系我们（ContactSection）**
   - 左侧联系信息，右侧表单（姓名、邮箱、电话、主题、留言）
8. **页脚（Footer）**
   - 品牌信息、快速链接、联系方式、社交媒体

**资源需求**：
- 将 `home-style/public/images/` 下的所有图片复制到 `static/core/img/`
- 若动物图片不足，可在 `media/` 下补充或复用现有动物模型图片

**验收标准**：
- 首页与提供的 7 张截图在视觉上一致
- 所有交互（悬停、滚动动画、计数器）正常工作
- 响应式适配移动端

---

### 第三批：认证模块（accounts）— 高优先级

**目标**：登录、注册、忘记密码、密码重置等页面与首页暖橙风格统一。

**具体工作**：
1. **重构 `accounts/auth_base.html`**
   - 从当前深色主题改为暖白/橙色主题
   - 保留左右分栏或居中卡片布局（参考 `home-style` 的简洁表单风格）
2. **重构 `accounts/login.html`**
   - 输入框使用新表单样式（圆角、暖橙聚焦 ring）
   - 按钮使用主按钮样式
   - 保留“忘记密码”和“立即注册”链接
3. **重构 `accounts/register.html`**
   - 账号注册 / 手机注册 Tab 切换保留
   - 表单字段样式统一
4. **重构 `accounts/password_reset_form.html`、`password_reset_confirm.html`、`password_reset_done.html`、`password_reset_complete.html`**
   - 统一使用 `auth_base.html` 的新样式
5. **重构 `accounts/profile.html`**
   - 个人资料页改为卡片式布局
   - 保留头像、信息编辑、密码修改功能

**验收标准**：
- 登录、注册、密码重置流程全部可正常使用
- 表单验证错误提示样式与新主题一致

---

### 第四批：动物模块（animals）

**目标**：动物列表、详情、救助申请页面风格统一。

**具体工作**：
1. **重构 `animals/list.html`**
   - 筛选栏（种类、健康状态、校区、救助状态）改为新表单样式
   - 动物网格卡片使用新 `cards.css` 样式（圆角、阴影、悬停放大）
   - 分页器改为新按钮样式
2. **重构 `animals/detail.html`**
   - 动物大图展示、信息卡片（品种、年龄、健康状态、性格）
   - 救助/领养按钮使用主按钮样式
   - 图片轮播/画廊
3. **重构 `animals/rescue_form.html`**
   - 救助申请表单统一为新表单样式
4. **重构 `animals/my_rescues.html`**
   - 我的救助列表改为卡片式布局

**验收标准**：
- 筛选、分页、详情查看、救助申请功能正常

---

### 第五批：领养模块（adoptions）

**目标**：领养列表、详情、申请页面风格统一。

**具体工作**：
1. **重构 `adoptions/list.html`**
   - 与 animals/list.html 风格保持一致（可领养动物列表）
   - 筛选栏、卡片网格、分页
2. **重构 `adoptions/detail.html`**
   - 动物信息 + 领养须知 + 申请按钮
3. **重构 `adoptions/apply_form.html`**
   - 领养申请表单使用新表单样式
4. **重构 `adoptions/mine.html`**
   - 我的领养记录卡片式展示

**验收标准**：
- 领养申请流程完整可用

---

### 第六批：活动模块（activities）

**目标**：活动列表、详情、报名页面风格统一。

**具体工作**：
1. **重构 `activities/list.html`**
   - 活动卡片网格（封面图、标题、时间、地点、状态、报名按钮）
   - 分页器
2. **重构 `activities/detail.html`**
   - 活动详情页：封面大图、活动信息、报名按钮、已报名人数

**验收标准**：
- 活动列表、详情查看、报名/取消报名功能正常

---

### 第七批：捐赠模块（donations）

**目标**：捐赠项目列表、详情、认捐页面风格统一。

**具体工作**：
1. **重构 `donations/list.html`**
   - 捐赠项目卡片网格（封面、标题、进度条、目标金额、标签）
   - 进度条使用暖橙渐变
2. **重构 `donations/detail.html`**
   - 项目详情：大图、描述、需求物品列表、认捐按钮
   - 物品列表表格改为卡片式或现代表格样式
3. **认捐交互优化**
   - 数量选择、备注输入框使用新表单样式

**验收标准**：
- 捐赠项目浏览、详情查看、认捐功能正常

---

### 第八批：志愿者模块（volunteers）

**目标**：社区列表、文章详情、帖子、志愿者申请页面风格统一。

**具体工作**：
1. **重构 `volunteers/community_list.html`**
   - 文章卡片 + 帖子列表
   - 文章区使用大图卡片，帖子区使用简洁列表/卡片
2. **重构 `volunteers/article_detail.html`**
   - 文章详情页：封面、标题、正文、标签
3. **重构 `volunteers/post_detail.html`**
   - 帖子详情 + 回复列表
4. **重构 `volunteers/apply_form.html`**
   - 志愿者申请表单使用新表单样式
5. **重构 `volunteers/mine.html`**（如有）
   - 我的志愿者信息卡片式展示

**验收标准**：
- 社区浏览、文章阅读、帖子互动、志愿者申请功能正常

---

### 第九批：通知模块（notifications）

**目标**：通知列表、详情页面风格统一。

**具体工作**：
1. **重构 `notifications/list.html`**
   - 通知列表改为简洁卡片或行列表样式
   - 已读/未读状态区分（如左侧橙色竖线表示未读）
2. **重构 `notifications/detail.html`**
   - 通知详情页简洁展示

**验收标准**：
- 通知列表、查看、标记已读功能正常

---

### 第十批：管理后台（admin）

**目标**：SimpleUI 后台或自定义 admin 模板风格统一。

**具体工作**：
1. **检查 `templates/admin/` 和 `static/admin/` 文件**
   - `dashboard.html`、`accounts-admin.css`、`dashboard.js` 等
2. **统一 admin 样式**
   - 如果使用了 SimpleUI，确保主题色与暖橙风格一致
   - 自定义 admin 页面（如用户批量导入）更新为新表单样式

**验收标准**：
- 管理后台各页面无样式崩坏，与前端风格协调

---

### 第十一批：README 与品牌收尾（最后完成）

**目标**：替换所有 DjangoHarness 开源品牌描述，建立 Street Pet Society 品牌。

**具体工作**：
1. **重写 `README.md`**
   - 删除所有 DjangoHarness 品牌和描述
   - 添加 Street Pet Society 品牌 logo（如 `static/accounts/brand/logo.png` 已存在，确认是否需要替换）
   - 简洁描述项目模块和功能（面向大学生流浪动物救助平台）
   - 添加项目故事/使命描述吸引用户
2. **重写 `README.en.md`**
   - 英文版与中文版内容对应
3. **品牌资产检查**
   - 确认 `static/accounts/brand/logo.png` 是否为 Street Pet Society 品牌图
   - 如不是，需替换为新的品牌 logo
4. **全站文案检查**
   - 替换残留的 DjangoHarness 品牌文案（如注册页的“加入 DjangoHarness”）

**验收标准**：
- README 中无任何 DjangoHarness 相关描述
- 全站品牌文案统一为 Street Pet Society / 流浪动物救助平台

---

## 执行顺序总览

| 批次 | 模块 | 优先级 | 前置依赖 |
|------|------|--------|----------|
| 1 | 基础设计系统 + 全局布局 | 🔴 最高 | 无 |
| 2 | 首页（core） | 🔴 最高 | 批次 1 |
| 3 | 认证（accounts） | 🟠 高 | 批次 1 |
| 4 | 动物（animals） | 🟡 中 | 批次 1 |
| 5 | 领养（adoptions） | 🟡 中 | 批次 1, 4 |
| 6 | 活动（activities） | 🟡 中 | 批次 1 |
| 7 | 捐赠（donations） | 🟡 中 | 批次 1 |
| 8 | 志愿者（volunteers） | 🟡 中 | 批次 1 |
| 9 | 通知（notifications） | 🟢 低 | 批次 1 |
| 10 | 管理后台（admin） | 🟢 低 | 批次 1 |
| 11 | README + 品牌收尾 | 🟢 最低 | 全部完成 |

---

## 关键风险与注意事项

1. **功能不变原则**：每批次重构后必须验证原有业务功能（表单提交、分页、筛选、权限控制）不受影响。
2. **图片资源**：`home-style` 中的图片需迁移到 `static/` 或 `media/`；动物图片优先复用数据库中已有图片。
3. **字体加载**：`ZCOOL XiaoWei` 和 `Manrope` 通过 Google Fonts CDN 加载，需确保国内网络可访问，或做本地字体回退。
4. **响应式**：每批次都要检查移动端适配，特别是导航栏折叠、卡片网格、表单布局。
5. **渐进式动画**：先完成静态样式，再逐步添加 Framer Motion 级别的动画（可用 CSS `scroll-timeline` 或轻量 JS 实现）。
