# 第 2 批（首页重构）：暖橙风格首页

## 实施内容

### 图片资源迁移
- 将 `home-style/app/public/images/` 下的全部 11 张图片复制到 `static/core/img/`
- 包含：hero-bg.jpg、about-volunteer.jpg、adopt-family.jpg、donate-support.jpg、volunteer-work.jpg、6 张宠物肖像图

### 首页 CSS 重构（`static/core/css/home.css`）
完全重写，从原压缩的绿色主题 CSS 改为暖橙主题的 10 大区块：

1. **Hero 区域** — 全屏背景图 + 左到右渐变遮罩 + 大标题 + 药丸形 CTA 按钮 + 底部滚动指示器动画
2. **关于我们** — 左文右图布局，eyebrow + 展示标题 + 统计数据（3 列）+ 星星装饰（CSS 浮动动画）+ 圆形图片边框
3. **服务区域** — 3 列网格，复用 `components/cards.css` 的 `.service-card`
4. **动物卡片** — 浅橙背景 + 水平滚动容器（scroll-snap）+ 左右滚动按钮 + 复用 `.pet-card`
5. **参与行动** — 3 列网格，复用 `.involve-card`（大图覆盖渐变 + 悬停放大）
6. **数据统计** — 橙色渐变背景 + 4 列图标 + 大号数字 + 响应式 2 列（移动端）
7. **联系区域** — 左信息（4 个联系项带图标）+ 右表单（2×2 网格 + 文本域 + 提交按钮）
8. **页脚** — 深色背景 + 4 列（品牌 / 快速链接 / 联系方式 / 社交媒体）+ 底部版权栏
9. **滚动揭示动画** — `.reveal` / `.reveal-left` / `.reveal-right` + `.is-visible` 状态切换
10. **响应式** — 移动端适配（堆叠布局、字体缩小、按钮全宽、统计 2 列）

### 首页模板重构（`apps/core/templates/core/home.html`）
完全重写，保留所有现有业务数据变量：

- **Hero**: 优先使用数据库 `banners` 图片，否则 fallback 到 `hero-bg.jpg`；CTA 链接到 `adoptions:list` 和 `#about`
- **关于我们**: 静态文案 + 使用数据库 `stats` 数据（rescued、volunteers）
- **服务**: 6 个静态服务卡片（动物救助、医疗救助、领养服务、社区教育、志愿者招募、绝育计划）
- **动物卡片**: 使用 `latest_animals` 数据，每个卡片展示 cover_image、名称、品种、校区、健康状态；无封面时 fallback 到占位图；左右按钮使用 JS `scrollBy`
- **参与行动**: 3 张卡片分别链接到 `adoptions:list`、`donations:list`、`volunteers:community`
- **数据统计**: 使用数据库 `stats`（rescued、adopted、donations、volunteers）
- **联系**: 静态联系信息 + 前端表单（内联 `submitContactForm` 显示成功提示，无后端提交）
- **页脚**: 品牌信息 + 导航链接 + 联系方式 + 社交媒体

### 首页脚本更新（`static/core/js/home.js`）
- 更新 IntersectionObserver 阈值和 rootMargin，支持 `.reveal`、`.reveal-left`、`.reveal-right` 三类动画
- 保留 DOMContentLoaded 事件监听

## 验证结果
- CSS 括号平衡：110 对，完全匹配
- 静态文件路径检查：8 个 `{% static %}` 引用全部存在
- 模板标签配对：`extends`/`endblock`、`for`/`endfor`、`with`/`endwith` 正确
- HTML 标签平衡：无未闭合标签（`<li` 误报来自 `<link` 正则匹配）

## 保留的业务数据
- `banners`、`quick_entries`、`welfare_posters`（海报系统）
- `latest_animals`（最新 6 只动物）
- `latest_activities`（最新 3 个活动）
- `urgent_items`（急需物资，4 项）
- `stats`（ rescued / adopted / volunteers / donations 计数）

## 待后续批次处理
- 首页数据区块与数据库的进一步联动（如服务数据、联系方式可配置化）
- 联系表单目前仅前端展示成功状态，如需后端提交需第三批或后续实现
- 滚动揭示动画可进一步升级为 CSS `scroll-timeline` 或 `view()` 函数以替代 JS
