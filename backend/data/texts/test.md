# 智能数据可视化与后端存储一体化实践

> 构建可扩展、可维护的现代数据展示系统

---

## 项目概述

本项目旨在实现一个**前后端一体化的数据内容展示平台**，结合 Vue 3 + TypeScript 前端框架与 PostgreSQL 后端数据库，支持富文本、多图展示、时间元数据及高效内容浏览体验。适用于技术博客、新闻资讯、项目日志等场景。

---

## 核心特性

- ✅ **响应式卡片布局**：使用 Element Plus `el-card` 构建美观、交互友好的信息流。
- ✅ **多图支持**：每条内容可关联多张图片，自动以画廊形式展示。
- ✅ **智能文本截断**：正文过长时自动折叠，提供“展开/收起”交互。
- ✅ **本地化时间显示**：日期与时间按中文格式（`zh-CN`）呈现。
- ✅ **类型安全**：全程使用 TypeScript 定义数据结构，确保开发可靠性。
- ✅ **Vite 静态资源管理**：通过 `new URL(..., import.meta.url)` 安全引用本地图片。

---

## 数据模型

### 前端接口定义（`test.ts`）

```ts
export interface Test {
  title: string;        // 标题
  main_text: string;    // 正文内容
  date: Date;           // 日期（如 2026-01-08）
  time: Date;           // 时间（如 14:30:00）
  img_src: string[];    // 图片 URL 数组
}
```

### 数据库表结构（PostgreSQL）

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    main_text TEXT NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    img_urls TEXT[] NOT NULL DEFAULT '{}'
);
```

> 💡 **建议**：生产环境优先存储图片 URL 而非二进制数据（`BYTEA`），以提升性能与可维护性。

---

## 关键实现细节

### 1. 图片资源引用（Vite）

```ts
// 正确方式：使用相对路径 + import.meta.url
new URL("../assets/preview.jpg", import.meta.url).href
```

避免使用绝对路径（如 `E:\\...`），确保构建后资源路径正确。

### 2. 长文本截断逻辑

- 默认显示 **3 行**正文。
- 超出部分自动省略，显示“展开”按钮。
- 点击后动态展开全文，按钮变为“收起”。

### 3. 响应式设计

- 支持桌面端与移动端（`@media (max-width: 600px)`）。
- 卡片悬停动效、阴影增强交互反馈。
- 图片画廊自动换行，适配不同屏幕宽度。

---

## 部署建议

| 环节 | 推荐方案 |
|------|--------|
| **前端** | Vite 构建 → Nginx 静态托管 |
| **后端 API** | FastAPI / Flask 提供 REST 接口 |
| **数据库** | PostgreSQL（云服务如 AWS RDS / 本地 Docker） |
| **图片存储** | 本地 `uploads/` 目录（开发）或 MinIO / S3（生产） |

---

## 未来优化方向

- 🔜 支持 Markdown 渲染正文
- 🔜 添加分页或无限滚动
- 🔜 实现搜索与标签分类
- 🔜 集成 ECharts 可视化嵌入
- 🔜 后台管理界面（CRUD 内容）

---

## 结语

通过将**类型安全的前端开发**与**结构化数据存储**紧密结合，我们不仅实现了内容的有效组织，更构建了一个可演进、易维护的技术基座。在数据驱动的时代，这样的系统将成为连接信息与洞察的重要桥梁。

> 📌 **源码结构示例**
> ```
> src/
> ├── assets/           # 静态资源
> ├── components/
> │   └── NewsList.vue  # 本文核心组件
> ├── types/
> │   └── test.ts       # TypeScript 接口定义
> └── views/
> ```