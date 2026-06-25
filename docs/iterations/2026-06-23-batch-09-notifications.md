# 第 9 批（通知模块）：暖橙主题重构

## 实施内容

### 新建 CSS（`static/notifications/css/notifications.css`）
暖橙主题通知样式：
1. **页面头部** — `section-kicker` + 大标题
2. **通知列表** — 行列表（白色卡片 + 阴影 + 悬停微上浮）；未读行左侧橙色竖线 + 橙色圆点标记；标题 + 日期 + 未读状态标签
3. **通知详情** — 居中窄布局（max-width 820px）；返回链接 + eyebrow + 标题 + 内容 + 底部分隔时间
4. **分页器** — 药丸按钮 + 页码显示

### 模板重构

#### `list.html`
- 保持：分页 + 循环 + 已读/未读判断
- 改进：`section-kicker` + 未读橙色标记（竖线 + 圆点 + 标签）+ 分页器 + 空状态

#### `detail.html`
- 保持：标题 + 内容 + 时间 + 自动标记已读（后端逻辑）
- 改进：返回链接 + eyebrow + 居中窄布局 + 时间格式化 + 底部分隔线

## 验证结果
- CSS 括号平衡：通过
- 旧 CSS 变量：无残留
- 品牌文案：无 "stray-animal-rescue-platform"

## 保留的业务逻辑
- `notification_list` 的用户隔离 + 分页（20 条/页）
- `notification_detail` 的 `recipient` 隔离 + 自动标记已读（`read_at`）
- `mark_read` 的 POST 提交 + 重定向到列表
