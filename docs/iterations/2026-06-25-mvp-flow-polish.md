# 2026-06-25 MVP 流程体验修复与模块丰富

## 问题

- 志愿者社区文章、帖子详情页使用 `{% static %}` 但未加载 `static` 模板标签，访问详情时报 `TemplateSyntaxError`。
- 救助、领养、志愿者、捐赠、活动模块列表页信息密度偏低，主要只有模块基础内容和筛选。
- 首页非首屏图片加载属性不完整，横向宠物滚动区域仍可继续降低对主滚动的影响。

## 修改

- 为 `volunteers/article_detail.html` 和 `volunteers/post_detail.html` 增加 `{% load static %}`，修复详情页模板错误。
- 在救助、领养、志愿者、捐赠、活动视图补充轻量统计、校区快照、推荐/急需条目等上下文。
- 在各模块列表页加入统一的模块摘要、流程、推荐或快照区域，延续当前暖橙、白卡、细分隔线视觉风格。
- 为列表动物图片、首页非首屏图片和空状态图片补充 `loading="lazy"`、`decoding="async"`。
- 为首页宠物横向滚动容器增加布局绘制隔离，减少横向滚动区对页面主滚动的重绘影响。
- 更新相关测试，覆盖详情页渲染、模块摘要区输出、当前首页文案和图片懒加载属性。

## 验证

- 通过：`uv run --no-sync ruff check apps base_framework celery_app tests manage.py`。
- 通过：`uv run --no-sync mypy apps base_framework celery_app tests manage.py`。
- 通过：`uv run --no-sync python manage.py check`。
- 通过：`uv run pytest -q`，67 passed。
- 注意：全仓库 `ruff format --check` 仍会提示既有 `base_framework/settings/base.py` 需要换行格式化；本批未纳入该无关格式化改动。
