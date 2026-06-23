# My Blog - 个人博客系统

一个基于 FastAPI + Vue3 + Docker 的现代化个人博客系统

## 技术栈

### 后端
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化 Python Web 框架
- [SQLite](https://www.sqlite.org/) - 轻量级数据库
- [Python 3.x](https://www.python.org/) - 编程语言

### 前端
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [TypeScript](https://www.typescriptlang.org/) - 强类型 JavaScript 超集
- [Element Plus](https://element-plus.org/) - Vue 3 组件库
- [Vite](https://vitejs.dev/) - 下一代前端构建工具
- [Vue Router](https://router.vuejs.org/) - Vue 官方路由

### 部署
- [Docker](https://www.docker.com/) - 容器化平台
- [Nginx](https://nginx.org/) - Web 服务器

## 项目结构

```
my_site/
├── backend/              # FastAPI 后端
│   ├── app.py            # 主应用文件
│   ├── requirements.txt  # Python依赖
│   ├── data/             # SQLite数据库文件存储
│   └── Dockerfile        # 后端Docker镜像配置
├── frontend/             # Vue3 前端
│   ├── src/
│   │   ├── api/          # API接口
│   │   ├── components/   # Vue组件
│   │   ├── router/       # 路由配置
│   │   ├── utils/        # 工具函数
│   │   └── views/        # 页面组件
│   ├── public/           # 静态资源
│   ├── Dockerfile        # 前端Docker镜像配置
│   └── package.json      # 前端依赖
├── nginx/                # Nginx配置
│   └── default.conf      # Nginx反向代理配置
└── docker-compose.yml    # Docker编排配置
```

## 功能特性

### 博客功能
- ✅ 文章发布与管理（CRUD）
- ✅ Markdown 内容支持
- ✅ 文章分类与标签
- ✅ 分页展示
- ✅ 文章阅读量统计
- ✅ 文章置顶功能
- ✅ 文章搜索
- ✅ 隐私控制（公开/私有）

### 个人资料
- ✅ 个人信息展示（昵称、头衔、简介等）
- ✅ 技术栈展示
- ✅ 联系方式展示
- ✅ 特色功能展示

### 资源中心
- ✅ 资源上传与管理
- ✅ 资源分类
- ✅ 资源下载保护（密码）
- ✅ 资源预览

### 订阅系统
- ✅ 邮件订阅
- ✅ 订阅状态管理

### 交互功能
- ✅ 快速发布文章
- ✅ 数据可视化（如需要）
- ✅ 响应式设计

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- Docker & Docker Compose

### 本地开发

#### 后端开发
```bash
cd backend
python app.py
```

后端服务将运行在 `http://localhost:8000`

#### 前端开发
```bash
cd frontend
npm install
npm run dev
```

前端服务将运行在 `http://localhost:5173`

### Docker 部署

#### 构建并启动
```bash
docker-compose up --build
```

#### 停止服务
```bash
docker-compose down
```

#### 查看日志
```bash
docker-compose logs -f
```

### 生产部署

1. 构建前端
```bash
cd frontend
npm run build
```

2. 构建后端 Docker 镜像
```bash
cd backend
docker build -t my-blog-backend .
```

3. 启动服务（修改 `docker-compose.yml` 配置后）
```bash
docker-compose up -d
```

### 配置说明

#### 数据库配置
后端使用 SQLite 数据库，数据库文件路径默认为：
```
backend/data/My_blog_texts.sqlite
```

可通过环境变量 `DATABASE_PATH` 自定义：
```yaml
environment:
  - DATABASE_PATH=/app/data/your_database.sqlite
```

#### API 端点

主要 API 端点：
- `GET /api/posts` - 获取文章列表
- `GET /api/posts/{id}` - 获取单篇文章
- `GET /api/categories` - 获取分类列表
- `GET /api/tags` - 获取标签列表
- `POST /api/resources/verify` - 验证资源密码
- `GET /api/profile` - 获取个人资料

更多 API 端点请参考 `backend/app.py`

## 开发指南

### 添加新文章
编辑 `backend/data/articles.csv` 或通过 API 创建

### 添加新功能
- 后端：在 `backend/app.py` 中添加路由和业务逻辑
- 前端：在 `frontend/src/views/` 中添加页面组件，在 `frontend/src/router/` 中配置路由

### 自定义样式
修改 `frontend/src/style.css` 进行全局样式配置

### ESLint/Prettier
根据项目需求配置代码规范工具

## 数据库操作

### 进入数据库
```python
import sqlite3
conn = sqlite3.connect('backend/data/My_blog_texts.sqlite')
```

### 常用 SQL 查询
```sql
-- 查看所有文章
SELECT * FROM articles;

-- 查看所有分类
SELECT * FROM categories;

-- 查看个人资料
SELECT * FROM profile;
```

## 常见问题

### 端口冲突
如果 80 端口被占用，修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:80"  # 将 80 改为 8080
```

### 前端构建失败
清除缓存后重新构建：
```bash
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

### 后端数据库连接问题
检查 `DATABASE_PATH` 环境变量是否正确配置，确保数据目录路径存在且可写

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- GitHub: [https://github.com/mgj-hyz](https://github.com/mgj-hyz)
- Email: contact@mgj-hyz.icu
- Blog: [https://mgj-hyz.icu](https://mgj-hyz.icu)

## 更新日志

### v1.0.0 (2026-06-23)
- 初始版本发布
- 完整的博客系统功能
- 支持 Docker 部署

---

**如有问题或建议，欢迎随时联系！**
