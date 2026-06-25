<p align="center">
  <img src="static/accounts/brand/logo.png" alt="Street Pet Society" width="120">
</p>

<p align="center"><strong>给流浪动物一个温暖的家</strong></p>

<p align="center">
  <img alt="Python 3.10-3.13" src="https://img.shields.io/badge/Python-3.10--3.13-3776AB">
  <img alt="Django 4.2" src="https://img.shields.io/badge/Django-4.2-0C4B33">
  <img alt="Celery 5" src="https://img.shields.io/badge/Celery-5-37814A">
  <img alt="Redis 6+" src="https://img.shields.io/badge/Redis-6%2B-DC382D">
  <img alt="MySQL 8" src="https://img.shields.io/badge/MySQL-8-4479A1">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-blue">
</p>

中文 | [English](README.en.md)

# 流浪动物救助平台

这是一个面向大学校园的流浪动物救助公益平台，致力于通过信息化手段连接爱心人士、志愿者、领养人和校园管理部门，为流浪动物提供救助、医疗、领养、捐赠等全方位服务。

## 功能模块

| 模块 | 说明 |
|------|------|
| 🏠 **首页** | 展示平台数据、最新动物、参与行动、联系方式 |
| 🔐 **用户认证** | 注册、登录、密码重置、个人资料管理 |
| 🐾 **动物救助** | 发布救助信息、审核救助申请、查看动物档案 |
| 🏡 **领养中心** | 浏览可领养动物、提交领养申请、管理领养关系 |
| 📅 **校园活动** | 发布活动、报名参与、管理活动记录 |
| 💝 **爱心捐赠** | 浏览捐赠项目、认捐物资、跟踪捐赠进度 |
| 🤝 **志愿者社区** | 社区文章、帖子分享、志愿者申请与管理 |
| 🔔 **通知中心** | 站内消息、自动标记已读 |
| ⚙️ **管理后台** | SimpleUI 后台、运营数据看板、用户批量导入 |

## 快速开始

环境要求：Python 3.10～3.13、uv。生产使用 MySQL 8.x 和 Redis 6+；本地默认使用 SQLite 数据库。

```bash
# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Python 并锁定版本
uv python install 3.10
uv python pin 3.10

# 安装依赖
uv sync --all-groups --locked

# 准备配置与数据库
cp .env.example .env
uv run python manage.py migrate

# 启动开发服务
uv run python manage.py runserver
```

访问主页 <http://127.0.0.1:8000/>，后台地址为 <http://127.0.0.1:8000/admin/>。

## 开发命令

```bash
make format  # 自动修复并格式化 Python、Markdown
make lint    # Ruff、mypy、mdformat、Django system check
make test    # pytest
make check   # lint + test
```

## 技术栈

- **后端**：Django 4.2 + Celery + Redis
- **落地页**： Next.js + React + TypeScript + Tailwind CSS
- **数据库**：MySQL 8（生产）/ SQLite（开发）
- **前端**：Django 模板 + 原生 CSS/JS（暖橙主题）
- **后台**：SimpleUI
- **任务队列**：Celery + Redis
- **代码质量**：Ruff、mypy、pytest

## 项目使命

> 每一只流浪动物都值得被温柔以待。我们相信，通过技术的力量，可以让更多人参与到动物保护中来，用爱心和行动改变每一个小生命的命运。

## License

本项目使用 [MIT License](LICENSE)。
