# 第 4 批（动物模块）：暖橙主题重构

## 实施内容

### CSS 重构（`static/animals/css/animals.css`）
从旧的单文件压缩绿色主题完全重写为暖橙主题：

1. **页面头部** — `section-kicker` + 大标题 + 副标题 + 行动按钮
2. **筛选栏** — 5 列网格（类型/健康/校区/状态/筛选按钮），白色卡片底板 + 圆角选择框 + 暖橙聚焦环 + 实心橙筛选按钮
3. **动物卡片网格** — 3 列响应式（平板 2 列，手机 1 列），复用暖橙卡片风格：圆角、阴影、悬停上浮、图片放大；状态标签使用浅橙背景；描述文字截断（2 行）
4. **动物详情页** — 返回链接 + 元信息点状分隔 + 图片画廊（悬停放大）+ 信息卡片网格（发现位置/性别/年龄）+ 描述段落 + 标签云
5. **救助申请表单** — 居中窄布局（max-width 760px），兼容 Django `form.as_p` 输出格式；输入框暖橙聚焦 + 帮助文本 + 错误列表
6. **我的救助列表** — 行列表（两栏：左信息 + 右状态），悬停左移反馈，状态标签使用浅橙背景
7. **分页器** — 居中，药丸形按钮 + 页码显示
8. **空状态** — 居中灰色提示

### 模板重构

#### `list.html`（动物列表）
- 保持：4 个筛选下拉框 + 分页逻辑 + 卡片循环 + 空状态
- 改进：新增 `section-lead` 副标题、空状态使用 `.empty-state` 样式、无图片时显示占位
- 按钮从 `.action--primary` 改为 `.btn`

#### `detail.html`（动物详情）
- 保持：返回链接、画廊、信息、标签、描述
- 改进：新增元信息区域（点状分隔）、信息卡片网格、返回链接带箭头动画
- 无图片时显示占位

#### `rescue_form.html`（发起救助）
- 保持：`form.as_p` + CSRF + 提交按钮
- 改进：新增 `section-kicker` + 副标题、按钮使用 `.btn--wide`

#### `my_rescues.html`（我的救助）
- 保持：申请列表 + 分页 + 状态 + 审核备注 + 已批准动物链接
- 改进：新增 `section-kicker`、右栏状态对齐、分页器

## 验证结果
- CSS 括号平衡：通过
- 模板标签配对：无 mismatch
- 品牌文案：无 "stray-animal-rescue-platform" 残留
- CSS 变量：无旧变量使用

## 保留的业务逻辑
- `animal_list` 视图的 4 个筛选参数（category/health/campus/status）+ 分页
- `animal_detail` 的 `is_published=True` 过滤
- `rescue_create` 的 `RescueRequestForm` + 事务 + `RescueRequestImage` 批量创建
- `my_rescues` 的申请人隔离 + 分页
- 所有模板中的 `{% csrf_token %}`、`{% url %}`、`page_obj` 逻辑完全保留
