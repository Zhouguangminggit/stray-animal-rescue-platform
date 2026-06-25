# 第 8 批（志愿者模块）：暖橙主题重构

## 实施内容

### CSS 重构（`static/volunteers/css/community.css`）
从旧的压缩绿色主题完全重写为暖橙主题：

1. **页面头部** — `section-kicker` + 大标题 + 副标题 + 操作按钮组（加入志愿者 + 发布帖子）
2. **社区文章卡片** — 3 列网格（平板 2 列，手机 1 列），白色卡片 + 阴影 + 悬停上浮；标题 + 摘要截断 3 行
3. **用户帖子行列表** — 行布局（左标题+内容 + 右作者+日期），白色卡片底板 + 悬停微上浮；内容截断 2 行
4. **文章/帖子详情** — 居中窄布局（max-width 820px），eyebrow + 大标题 + 元信息（点状分隔）+ 封面图（圆角）+ 内容段落
5. **举报区域** — `<details>` 折叠面板，灰色摘要文字，展开后显示表单（白色卡片 + 阴影）；仅登录用户可见
6. **通用表单** — 居中窄布局（max-width 760px），兼容 `form.as_p`；输入框暖橙聚焦 + 帮助文本 + 错误列表；宽按钮提交
7. **我的志愿者页面** — 分区标题（带底边框）；志愿者状态标签（浅橙）；技能/时间信息行；申请记录行列表；我的帖子行列表
8. **分页器** — 药丸按钮 + 页码显示
9. **响应式** — 移动端堆叠、按钮全宽、行列表单列

### 模板重构

#### `community_list.html`
- 保持：头部操作按钮 + 文章卡片（前 6 篇）+ 帖子行列表（分页）+ FAQ
- 改进：新增 `section-kicker` + 副标题、分页器（原模板缺失）、空状态样式

#### `article_detail.html`
- 保持：标题 + 摘要 + 封面图 + 内容
- 改进：eyebrow 标签、封面图圆角大、居中窄布局

#### `post_detail.html`
- 保持：标题 + 作者 + 内容 + 举报表单（仅登录）
- 改进：元信息区域（点状分隔）、举报区域改为 `<details>` 折叠面板

#### `form.html`（帖子发布 + 志愿者申请共用）
- 保持：`form.as_p` + CSRF + 提交按钮 + `multipart` 支持
- 改进：eyebrow + 标题、宽按钮、表单样式统一

#### `mine.html`
- 保持：志愿者状态 + 申请记录 + 我的帖子
- 改进：分区标题 + 空状态 + 申请时间格式化 + 状态标签

## 验证结果
- CSS 括号平衡：通过
- 旧 CSS 变量：无残留
- 模板标签配对：无 mismatch
- 品牌文案：无 "stray-animal-rescue-platform"

## 保留的业务逻辑
- `community_list` 的 articles（前 6 篇）+ posts（分页，12 条/页）+ FAQ
- `article_detail` 的 `is_published=True` + `published_at__isnull=False` 过滤
- `post_detail` 的 `is_hidden=False` + `report_form` + 举报表单（仅登录）
- `post_create` 的 `CommunityPostForm` + `author` 自动设置 + 成功消息
- `report_post` 的 `CommunityReportForm` + `IntegrityError` 处理
- `volunteer_apply` 的 `VolunteerApplicationForm` + 重复申请检查 + `multipart`
- `mine` 的 `applications` + `profile` + `posts` 数据隔离
