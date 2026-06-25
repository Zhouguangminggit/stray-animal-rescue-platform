# 第 5 批（领养模块）：暖橙主题重构

## 实施内容

### CSS 重构（`static/adoptions/css/adoptions.css`）
从旧的压缩绿色主题完全重写为暖橙主题：

1. **领养详情页** — 双栏布局（左 2fr 内容 + 右 1fr 侧边栏），侧边栏 `position: sticky` + 白色卡片 + 阴影；表单输入框暖橙聚焦；领养状态标签使用浅橙背景；登录按钮/提交按钮全宽；已领养状态显示灰色提示
2. **我的领养页** — 居中窄布局（max-width 900px），分区标题带底边框；领养关系行和申请记录行统一样式（左信息 + 右状态标签），悬停左移反馈
3. **响应式** — 移动端双栏变单栏，侧边栏取消 sticky

### 模板重构

#### `list.html`
- 保持：4 个筛选下拉框（类型/健康/校区/状态）+ 分页 + 卡片网格
- 改进：复用 `animals/css/animals.css` 的卡片、筛选栏、分页样式；新增 `selected` 状态保持（补全原模板缺失的筛选记忆）；新增空状态占位；按钮使用 `.btn--secondary`
- 注意：`apply_form.html` 不存在，领养申请直接在 `detail.html` 侧边栏提交

#### `detail.html`
- 保持：左内容（返回链接、标题、画廊、描述）+ 右侧边栏（领养状态、申请表单/登录按钮/已领养提示）
- 改进：元信息使用点状分隔；返回链接带箭头动画；表单兼容 `form.as_p`；无图片时显示占位
- 业务逻辑完全保留：未登录显示登录按钮并带 `next` 跳转；已领养显示提示；`available` 状态显示申请表单

#### `mine.html`
- 保持：领养关系列表 + 申请记录列表
- 改进：新增 `section-kicker`；空状态使用 `.empty-state`；日期格式化

## 验证结果
- CSS 括号平衡：通过
- 旧 CSS 变量：无残留
- 模板标签配对：无 mismatch
- 品牌文案：无 "stray-animal-rescue-platform"

## 保留的业务逻辑
- `adoption_list` 的 4 个筛选参数 + 分页（12 条/页）
- `adoption_detail` 的 `is_published=True` + `adoption_status` 过滤 + `AdoptionApplicationForm` 传递
- `apply` 的 POST 提交 + `submit_adoption_application` 服务调用 + 错误/成功消息
- `mine` 的 `relationships` + `applications` 数据隔离
