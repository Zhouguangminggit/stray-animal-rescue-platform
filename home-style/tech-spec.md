# 流浪动物救助平台 - 技术规格

## 项目概述

基于 Next.js + React + TypeScript + Tailwind CSS 构建的流浪动物救助平台首页。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 15.x | 框架 |
| React | 19.x | UI 库 |
| TypeScript | 5.x | 类型系统 |
| Tailwind CSS | 3.x | 样式 |
| shadcn/ui | latest | UI 组件库 |
| Framer Motion | 11.x | 动画库 |
| Lucide React | latest | 图标库 |
| Google Fonts | - | ZCOOL XiaoWei, Manrope, Caveat |

## 组件清单

### shadcn/ui 组件
| 组件 | 用途 |
|------|------|
| Button | 按钮（主按钮、次要按钮） |
| Input | 表单输入框 |
| Textarea | 多行文本输入 |
| Select | 下拉选择（表单主题） |
| Dialog | 模态框（可选） |
| Sheet | 移动端侧边抽屉菜单 |
| Label | 表单标签 |

### 自定义组件
| 组件 | 用途 | 位置 |
|------|------|------|
| Navbar | 导航栏（透明→毛玻璃滚动效果） | app/sections/Navbar.tsx |
| HeroSection | 英雄区（全屏背景+标题+CTA） | app/sections/HeroSection.tsx |
| AboutSection | 关于我们（左文右图+统计） | app/sections/AboutSection.tsx |
| ServicesSection | 服务展示（6卡片网格） | app/sections/ServicesSection.tsx |
| PetsSection | 待领养动物（水平滚动卡片） | app/sections/PetsSection.tsx |
| GetInvolvedSection | 参与救助（3大图卡片） | app/sections/GetInvolvedSection.tsx |
| StatsSection | 数据统计（4数字计数动画） | app/sections/StatsSection.tsx |
| ContactSection | 联系我们（信息+表单） | app/sections/ContactSection.tsx |
| Footer | 页脚 | app/sections/Footer.tsx |
| AnimatedSection | 滚动揭示动画包装器 | app/components/AnimatedSection.tsx |
| CountUp | 数字计数动画 | app/components/CountUp.tsx |
| GradientText | 渐变文字效果 | app/components/GradientText.tsx |
| ServiceCard | 服务卡片 | app/components/ServiceCard.tsx |
| PetCard | 动物卡片 | app/components/PetCard.tsx |
| InvolveCard | 参与卡片 | app/components/InvolveCard.tsx |
| StarDecoration | SVG星星装饰 | app/components/StarDecoration.tsx |

## 动画实现方案

| 动画 | 库 | 实现方式 | 复杂度 |
|------|------|----------|--------|
| 页面加载淡入 | Framer Motion | initial/animate + transition | 低 |
| 滚动揭示动画 | Framer Motion | whileInView + viewport | 中 |
| 导航栏滚动效果 | React state + CSS | useScroll hook + 条件样式 | 中 |
| 按钮悬停效果 | Tailwind CSS | hover: 类 + transition | 低 |
| 卡片悬停效果 | Tailwind CSS | hover: 类 + transition | 低 |
| 数字计数动画 | Framer Motion | useMotionValue + useTransform + animate | 中 |
| 图片悬停放大 | Tailwind CSS | hover:scale-105 + transition | 低 |
| 星星浮动装饰 | Framer Motion | animate + infinite repeat | 低 |
| 水平滚动卡片 | CSS | overflow-x-auto + scroll-snap | 低 |
| 表单聚焦效果 | Tailwind CSS | focus: 类 + ring | 低 |

## 项目结构

```
/mnt/agents/output/my-app/
├── app/
│   ├── sections/          # 页面区块组件
│   │   ├── Navbar.tsx
│   │   ├── HeroSection.tsx
│   │   ├── AboutSection.tsx
│   │   ├── ServicesSection.tsx
│   │   ├── PetsSection.tsx
│   │   ├── GetInvolvedSection.tsx
│   │   ├── StatsSection.tsx
│   │   ├── ContactSection.tsx
│   │   └── Footer.tsx
│   ├── components/        # 可复用组件
│   │   ├── AnimatedSection.tsx
│   │   ├── CountUp.tsx
│   │   ├── GradientText.tsx
│   │   ├── ServiceCard.tsx
│   │   ├── PetCard.tsx
│   │   ├── InvolveCard.tsx
│   │   └── StarDecoration.tsx
│   ├── globals.css        # 全局样式 + Tailwind
│   ├── layout.tsx         # 根布局（字体加载）
│   └── page.tsx           # 首页（组合所有区块）
├── components/
│   └── ui/                # shadcn/ui 组件
├── public/
│   └── images/            # 静态图片资源
├── lib/
│   └── utils.ts           # 工具函数
├── next.config.js
├── tailwind.config.ts
└── package.json
```

## 依赖安装清单

```bash
# shadcn 组件
npx shadcn add button input textarea select sheet label

# 动画库
npm install framer-motion

# 图标库 (shadcn 已包含)
# lucide-react
```

## 颜色配置 (tailwind.config.ts)

```typescript
colors: {
  primary: {
    DEFAULT: '#FF8C42',
    dark: '#E56A21',
    light: '#FFA726',
  },
  accent: '#FF7043',
  dark: '#2D2A26',
  'warm-white': '#FFF8F0',
  'light-orange': '#FFF0E0',
  'border-orange': '#FFE0C0',
}
```

## 字体配置

在 layout.tsx 中使用 next/font/google 加载：
- Manrope (400, 500, 600, 700)
- Caveat (400)
- ZCOOL XiaoWei (400) - 通过 @import 从 Google Fonts CDN 加载

## 响应式断点

使用 Tailwind 默认断点：
- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px

## 图片资源

所有图片放置在 public/images/ 目录：
- hero-bg.jpg - 英雄区背景
- about-volunteer.jpg - 关于我们
- adopt-family.jpg - 领养卡片
- donate-support.jpg - 捐赠卡片
- volunteer-work.jpg - 志愿者卡片
- pet-doudou.jpg ~ pet-xueqiu.jpg - 6只动物肖像

## 注意事项

1. 使用 `use client` 指令：所有包含动画和交互的组件需要标记为客户端组件
2. Framer Motion 的 `whileInView` 用于滚动触发动画，设置 `once: true` 避免重复触发
3. 计数动画使用 Framer Motion 的 `useInView` + `useMotionValue` + `animate`
4. 导航栏滚动检测使用 `useEffect` + `scroll` 事件监听
5. 表单提交使用客户端状态管理，显示成功提示
6. 所有过渡动画支持 `prefers-reduced-motion` 媒体查询
