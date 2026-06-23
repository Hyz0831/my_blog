import sqlite3
import os
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from pathlib import Path
import json

# --- 配置 ---
DB_PATH = os.getenv(
    "DATABASE_PATH",
    str(Path(__file__).parent /"data"/"My_blog_texts.sqlite")
)
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)


def init_db():
    """初始化数据库，创建缺失的表"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # users 用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")

        # subscriptions 订阅表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                status TEXT DEFAULT 'active',
                subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sub_email ON subscriptions(email)")

        # categories 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                slug TEXT NOT NULL UNIQUE,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # articles 文章表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                content_format TEXT DEFAULT 'markdown',
                summary TEXT,
                cover_img TEXT,
                tags TEXT DEFAULT '[]',
                status TEXT DEFAULT 'draft',
                visibility TEXT DEFAULT 'public',
                is_top INTEGER DEFAULT 0,
                category_id INTEGER,
                slug TEXT,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                publish_time TIMESTAMP,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_author ON articles(author_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_visibility ON articles(visibility)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_publish_time ON articles(publish_time DESC)")
        
        # resources 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                experience TEXT,
                company TEXT,
                location TEXT,
                skills TEXT DEFAULT '[]',
                description TEXT,
                cover_img TEXT,
                file_path TEXT,
                filename TEXT,
                password TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # profile 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                nickname TEXT DEFAULT 'HYZ',
                avatar TEXT DEFAULT '/default-avatar.png',
                title TEXT DEFAULT '全栈开发者',
                subtitle TEXT DEFAULT '热爱技术，分享知识',
                bio TEXT DEFAULT '',
                tech_stack TEXT DEFAULT '[]',
                contacts TEXT DEFAULT '[]',
                features TEXT DEFAULT '[]',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 插入默认分类数据（如果为空）
        cursor.execute("SELECT COUNT(*) as cnt FROM categories")
        if cursor.fetchone()["cnt"] == 0:
            default_categories = [
                ('前端开发', 'frontend', 1),
                ('后端开发', 'backend', 2),
                ('DevOps', 'devops', 3),
                ('技术随笔', 'essay', 4),
                ('开源项目', 'opensource', 5),
            ]
            cursor.executemany(
                "INSERT INTO categories (name, slug, sort_order) VALUES (?, ?, ?)",
                default_categories
            )
        
        # 插入默认 profile 数据（如果为空）
        cursor.execute("SELECT COUNT(*) as cnt FROM profile")
        if cursor.fetchone()["cnt"] == 0:
            import json as _json
            cursor.execute("""
                INSERT INTO profile (nickname, avatar, title, subtitle, bio, tech_stack, contacts, features)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'HYZ', '/default-avatar.png', '全栈开发者', '热爱技术，分享知识',
                '一个热爱编程的开发者，专注于 Web 全栈开发和开源项目。',
                _json.dumps([
                    {'category': '前端', 'items': ['Vue.js', 'TypeScript', 'Element Plus', 'Vite']},
                    {'category': '后端', 'items': ['Python', 'FastAPI', 'SQLite', 'Node.js']},
                    {'category': '工具', 'items': ['Docker', 'Git', 'Nginx', 'VS Code']},
                    {'category': '其他', 'items': ['Linux', 'CI/CD', '云原生']}
                ]),
                _json.dumps([
                    {'platform': 'GitHub', 'url': 'https://github.com/mgj-hyz', 'icon': 'github'},
                    {'platform': 'Email', 'url': 'mailto:contact@mgj-hyz.icu', 'icon': 'email'},
                    {'platform': '博客', 'url': 'https://mgj-hyz.icu', 'icon': 'blog'}
                ]),
                _json.dumps([
                    {'title': '快速响应', 'description': '及时回复每一条消息和评论', 'icon': 'chat-dot-round'},
                    {'title': '持续学习', 'description': '保持对新技术的热情和学习动力', 'icon': 'reading'},
                    {'title': '开源贡献', 'description': '积极参与开源社区和项目贡献', 'icon': 'star'}
                ])
            ))
        
        conn.commit()
        print("✅ 数据库初始化完成")


# --- 数据库连接工具 ---
@contextmanager
def get_db_connection():
    """
    数据库连接上下文管理器
    关键优化：设置 row_factory = sqlite3.Row，使结果可以通过列名访问（类似字典）
    """
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row  # <--- 核心修改
    try:
        yield conn
    finally:
        conn.close()


def dict_from_row(row):
    """将 sqlite3.Row 转换为普通字典，方便 JSON 序列化"""
    if row is None:
        return None
    return dict(zip(row.keys(), row))


def dicts_from_rows(rows):
    """将 sqlite3.Row 列表转换为字典列表"""
    return [dict_from_row(row) for row in rows]


# --- 业务逻辑类 ---

class Get_Posts:
    def get_posts(self, page=1, page_size=8):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # 1. 获取总数
                cursor.execute("SELECT COUNT(*) as count FROM articles WHERE visibility = 'public'")
                total = cursor.fetchone()["count"]

                # 2. 计算分页
                offset = (page - 1) * page_size

                # 3. ✅ 修复：使用紧凑的 SQL 语句，避免多行字符串可能的解析问题
                # 注意：确保字段名与数据库完全一致
                query = (
                    "SELECT id, author_id as user_id, title, content, "
                    "content_format as content_type, summary, cover_img, "
                    "tags, status, visibility, is_top, "
                    "publish_time as created_at, update_time as updated_at "
                    "FROM articles "
                    "WHERE visibility = 'public' "
                    "ORDER BY update_time DESC "
                    "LIMIT ? OFFSET ?"
                )

                # 调试打印：查看最终执行的 SQL（可选，生产环境可删除）
                # print(f"Executing SQL: {query}")
                # print(f"Params: {page_size}, {offset}")

                cursor.execute(query, (page_size, offset))
                rows = cursor.fetchall()

                # 转换为字典列表
                data = dicts_from_rows(rows)

                return {
                    "code": 200,
                    "msg": "success",
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "data": data
                }
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"code": 500, "msg": f"Server Error: {str(e)}", "data": []}


class Get_Post:
    def get_post(self, post_id):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # 1. 查询文章
                cursor.execute("SELECT * FROM articles WHERE id = ?", (post_id,))
                row = cursor.fetchone()
                if not row:
                    return {"code": 404, "msg": "Post not found", "data": None}

                # 2. 增加文章阅读量
                cursor.execute("UPDATE articles SET views = views + 1 WHERE id = ?", (post_id,))

                # 3. 记录独立访客 (IP 去重 + 更新最后访问时间)
                # 注：实际 IP 需通过路由层传入，此处使用占位值
                # 实际部署时应修改 get_post 方法签名，接收 request: Request 参数
                ip_address = "127.0.0.1"  # 占位值，实际应使用 get_client_ip(request)
                cursor.execute("""
                               INSERT INTO site_visits (ip_address)
                               VALUES (?) ON CONFLICT(ip_address) DO
                               UPDATE SET
                                   visit_count = visit_count + 1,
                                   last_visit = CURRENT_TIMESTAMP
                               """, (ip_address,))

                conn.commit()
                return {"code": 200, "msg": "success", "data": dict_from_row(row)}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": None}

class Update_Post:
    def update_post(self, post_id, **kwargs):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # 过滤掉 None 值
                update_fields = []
                params = []

                # 允许更新的字段白名单
                allowed_fields = ['title', 'content', 'tags', 'summary', 'cover_img', 'status', 'visibility',
                                  'category_id', 'slug']

                for key, value in kwargs.items():
                    if key in allowed_fields and value is not None:
                        update_fields.append(f"{key} = ?")
                        params.append(value)

                if not update_fields:
                    return {"code": 400, "msg": "No valid fields to update", "data": None}

                # 自动更新更新时间
                update_fields.append("updated_at = CURRENT_TIMESTAMP")

                sql = f"UPDATE articles SET {', '.join(update_fields)} WHERE id = ?"
                params.append(post_id)

                cursor.execute(sql, params)
                conn.commit()

                if cursor.rowcount == 0:
                    return {"code": 404, "msg": "Post not found or no changes made", "data": None}

                return {"code": 200, "msg": "success", "data": None}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": None}


class Delete_Post:
    def delete_post(self, post_id):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM articles WHERE id = ?", (post_id,))
                conn.commit()
                return {"code": 200, "msg": "success", "data": None}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": None}


class Get_Categories:
    def get_categories(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, slug,
                           (SELECT COUNT(*) FROM articles WHERE category_id = c.id AND visibility = 'public') as count
                    FROM categories c ORDER BY sort_order ASC, id ASC
                """)
                rows = cursor.fetchall()
                data = dicts_from_rows(rows)
                return {"code": 200, "msg": "success", "data": data}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": []}


class Get_Tags:
    def get_tags(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                tags_dict = {}
                cursor.execute("SELECT id, tags FROM articles WHERE visibility = 'public' AND tags IS NOT NULL")
                rows = cursor.fetchall()
                for row in rows:
                    raw_tags = row["tags"]
                    tag_list = self._parse_tags(raw_tags)
                    for tag in tag_list:
                        clean_tag = tag.strip().strip('"\'')
                        if clean_tag and clean_tag not in tags_dict:
                            tags_dict[clean_tag] = {
                                "name": clean_tag,
                                "slug": clean_tag.lower().replace(" ", "-"),
                                "count": 0
                            }
                        if clean_tag:
                            tags_dict[clean_tag]["count"] += 1
                data = sorted(tags_dict.values(), key=lambda x: x["count"], reverse=True)
                for i, item in enumerate(data):
                    item["id"] = i + 1
                return {"code": 200, "msg": "success", "data": data}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"code": 500, "msg": str(e), "data": []}

    @staticmethod
    def _parse_tags(raw_tags):
        if isinstance(raw_tags, list):
            return [str(t) for t in raw_tags]
        if not isinstance(raw_tags, str) or not raw_tags.strip():
            return []
        stripped = raw_tags.strip()
        if (stripped.startswith('[') and stripped.endswith(']')) or \
           (stripped.startswith('{') and stripped.endswith('}')):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return [str(t).strip() for t in parsed if t]
                return [str(parsed)]
            except (json.JSONDecodeError, TypeError):
                pass
        separators_pattern = r'[,;，；|\/\\]+'
        import re
        parts = re.split(separators_pattern, stripped)
        return [p.strip() for p in parts if p.strip()]


class Get_Recent_Posts:
    def get_recent_posts(self, limit=5):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                query = (
                    "SELECT id, author_id as user_id, title, content, "
                    "content_format as content_type, summary, cover_img, "
                    "tags, status, visibility, is_top, "
                    "publish_time as created_at, update_time as updated_at, views "
                    "FROM articles WHERE visibility = 'public' "
                    "ORDER BY publish_time DESC LIMIT ?"
                )
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                data = dicts_from_rows(rows)
                return {"code": 200, "msg": "success", "data": data}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": []}


class Get_Top_Posts:
    def get_top_posts(self, limit=5):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                query = (
                    "SELECT id, author_id as user_id, title, content, "
                    "content_format as content_type, summary, cover_img, "
                    "tags, status, visibility, is_top, "
                    "publish_time as created_at, update_time as updated_at, views "
                    "FROM articles WHERE visibility = 'public' "
                    "ORDER BY views DESC LIMIT ?"
                )
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                data = dicts_from_rows(rows)
                return {"code": 200, "msg": "success", "data": data}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": []}


class Get_Resources:
    def get_resources(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, role, experience, company, location,
                           skills, description, cover_img, file_path, filename,
                           CASE WHEN password IS NOT NULL AND password != '' THEN 1 ELSE 0 END as has_password
                    FROM resources ORDER BY id DESC
                """)
                rows = cursor.fetchall()
                data = dicts_from_rows(rows)
                for item in data:
                    if isinstance(item.get("skills"), str):
                        item["skills"] = json.loads(item["skills"])
                return {"code": 200, "msg": "success", "data": data}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": []}


class Verify_Resource_Password:
    def verify_password(self, resource_id: int, password: str):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password, file_path FROM resources WHERE id = ?", (resource_id,))
                row = cursor.fetchone()
                if not row:
                    return {"code": 404, "msg": "资源不存在", "data": None}
                if row["password"] and row["password"] != password:
                    return {"code": 401, "msg": "密码错误", "data": None}
                import secrets
                token = secrets.token_urlsafe(32)
                return {
                    "code": 200, "msg": "验证成功",
                    "data": {"access_token": token, "file_path": row["file_path"]}
                }
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": None}


class Get_Profile:
    def get_profile(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM profile LIMIT 1")
                row = cursor.fetchone()
                if row:
                    data = dict_from_row(row)
                    if isinstance(data.get("tech_stack"), str):
                        data["tech_stack"] = json.loads(data["tech_stack"])
                    if isinstance(data.get("contacts"), str):
                        data["contacts"] = json.loads(data["contacts"])
                    if isinstance(data.get("features"), str):
                        data["features"] = json.loads(data["features"])
                    return {"code": 200, "msg": "success", "data": data}
                else:
                    default_profile = {
                        "nickname": "HYZ", "avatar": "/default-avatar.png",
                        "title": "全栈开发者", "subtitle": "热爱技术，分享知识",
                        "bio": "一个热爱编程的开发者",
                        "tech_stack": [
                            {"category": "前端", "items": ["Vue.js", "TypeScript", "Element Plus"]},
                            {"category": "后端", "items": ["Python", "FastAPI", "SQLite"]},
                            {"category": "工具", "items": ["Docker", "Git", "Nginx"]}
                        ],
                        "contacts": [
                            {"platform": "GitHub", "url": "https://github.com", "icon": "github"},
                            {"platform": "Email", "url": "mailto:example@email.com", "icon": "email"}
                        ],
                        "features": [
                            {"title": "快速响应", "description": "及时回复每一条消息", "icon": "chat-dot-round"},
                            {"title": "持续学习", "description": "保持对新技术的热情", "icon": "reading"},
                            {"title": "开源贡献", "description": "积极参与开源项目", "icon": "star"}
                        ]
                    }
                    return {"code": 200, "msg": "success", "data": default_profile}
        except Exception as e:
            return {"code": 500, "msg": str(e), "data": None}


# --- FastAPI 应用 ---

app = FastAPI(title="Blog API", version="1.0.0")

init_db()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://mgj-hyz.icu,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Requested-With"],
)

# 使用环境变量设置 API_KEY，生产环境必须修改默认值
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    import secrets
    API_KEY = secrets.token_urlsafe(32)
    print(f"⚠️  警告：未设置 API_KEY 环境变量，已生成临时密钥：{API_KEY[:8]}...")
    print("   请在生产环境中设置 API_KEY 环境变量以确保安全！")

from fastapi import Depends, Header, Request, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

# JWT 配置
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> Optional[Dict]:
    """从 JWT token 获取当前用户信息"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return {"username": username, "role": payload.get("role", "user")}
    except jwt.PyJWTError:
        return None

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(request: Request) -> Optional[Dict]:
    """从请求头获取当前用户信息（使用 JWT）"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return await get_current_user_from_token(token)


# --- Pydantic Models ---

class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class CreatePostRequest(BaseModel):
    title: str
    content: str
    content_format: Optional[str] = "markdown"
    summary: Optional[str] = None
    cover_img: Optional[str] = None
    tags: Optional[str] = None
    category_id: Optional[int] = None
    slug: Optional[str] = None
    visibility: Optional[str] = "draft"

class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    summary: Optional[str] = None
    cover_img: Optional[str] = None
    status: Optional[str] = None
    visibility: Optional[str] = None
    category_id: Optional[int] = None
    slug: Optional[str] = None

class APIResponse(BaseModel):
    code: int
    msg: str
    data: Any = None
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


async def get_client_ip(request: Request) -> str:
    """获取客户端真实 IP"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


# --- Routes ---

@app.get("/api/posts", response_model=APIResponse)
async def get_all_posts(page: int = 1, page_size: int = 8):
    service = Get_Posts()
    result = service.get_posts(page=page, page_size=page_size)
    return result


@app.get("/api/posts/recent")
async def get_recent_posts_api(limit: int = 5):
    """📄 获取最近发布的文章 - 必须在 {post_id} 之前注册！"""
    service = Get_Recent_Posts()
    result = service.get_recent_posts(limit=limit)
    return result


@app.get("/api/posts/top")
async def get_top_posts_api(limit: int = 5):
    """🔥 获取热门文章（按阅读量排序）- 必须在 {post_id} 之前注册！"""
    service = Get_Top_Posts()
    result = service.get_top_posts(limit=limit)
    return result


class Get_Posts_By_Category:
    def get_posts_by_category(self, category_slug: str, page=1, page_size=8):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM categories WHERE slug = ? OR name = ? OR id = ?", (category_slug, category_slug, category_slug))
                cat_row = cursor.fetchone()
                if not cat_row:
                    return {"code": 200, "msg": "success", "total": 0, "page": page, "page_size": page_size, "data": []}
                cat_id = cat_row["id"]
                cursor.execute("SELECT COUNT(*) as count FROM articles WHERE visibility = 'public' AND category_id = ?", (cat_id,))
                total = cursor.fetchone()["count"]
                offset = (page - 1) * page_size
                query = (
                    "SELECT id, author_id as user_id, title, content, "
                    "content_format as content_type, summary, cover_img, "
                    "tags, status, visibility, is_top, "
                    "publish_time as created_at, update_time as updated_at "
                    "FROM articles "
                    "WHERE visibility = 'public' AND category_id = ? "
                    "ORDER BY is_top DESC, update_time DESC "
                    "LIMIT ? OFFSET ?"
                )
                cursor.execute(query, (cat_id, page_size, offset))
                rows = cursor.fetchall()
                data = dicts_from_rows(rows)
                return {"code": 200, "msg": "success", "total": total, "page": page, "page_size": page_size, "data": data}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"code": 500, "msg": f"Server Error: {str(e)}", "data": []}


@app.get("/api/categories/{category_slug}/posts")
async def get_posts_by_category_api(category_slug: str, page: int = 1, size: int = 8):
    """📁 按分类筛选文章 - 必须在 /api/posts/{post_id} 之前注册！"""
    service = Get_Posts_By_Category()
    result = service.get_posts_by_category(category_slug=category_slug, page=page, page_size=size)
    return result


class Get_Posts_By_Tag:
    @staticmethod
    def _parse_tags(raw_tags):
        if isinstance(raw_tags, list):
            return [str(t).strip().strip('"\'') for t in raw_tags]
        if not isinstance(raw_tags, str) or not raw_tags.strip():
            return []
        stripped = raw_tags.strip()
        if (stripped.startswith('[') and stripped.endswith(']')) or \
           (stripped.startswith('{') and stripped.endswith('}')):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return [str(t).strip().strip('"\'') for t in parsed if t]
                return [str(parsed).strip()]
            except (json.JSONDecodeError, TypeError):
                pass
        import re
        parts = re.split(r'[,;，；|\/\\]+', stripped)
        return [p.strip().strip('"\'') for p in parts if p.strip()]

    def get_posts_by_tag(self, tag_name: str, page=1, page_size=8):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                clean_tag = tag_name.strip().strip('"\'[]')
                cursor.execute("SELECT id, tags FROM articles WHERE visibility = 'public' AND tags IS NOT NULL")
                rows = cursor.fetchall()
                matching_ids = []
                for row in rows:
                    tag_list = self._parse_tags(row["tags"])
                    if any(clean_tag.lower() == t.lower() for t in tag_list):
                        matching_ids.append(row["id"])
                total = len(matching_ids)
                if total == 0:
                    return {"code": 200, "msg": "success", "total": 0, "page": page, "page_size": page_size, "data": []}
                offset = (page - 1) * page_size
                placeholders = ','.join(['?'] * len(matching_ids[offset:offset + page_size]))
                query = (
                    f"SELECT id, author_id as user_id, title, content, "
                    f"content_format as content_type, summary, cover_img, "
                    f"tags, status, visibility, is_top, "
                    f"publish_time as created_at, update_time as updated_at "
                    f"FROM articles "
                    f"WHERE id IN ({placeholders}) "
                    f"ORDER BY is_top DESC, update_time DESC"
                )
                cursor.execute(query, matching_ids[offset:offset + page_size])
                data = dicts_from_rows(cursor.fetchall())
                return {"code": 200, "msg": "success", "total": total, "page": page, "page_size": page_size, "data": data}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"code": 500, "msg": f"Server Error: {str(e)}", "data": []}


@app.get("/api/tags/{tag_name}/posts")
async def get_posts_by_tag_api(tag_name: str, page: int = 1, size: int = 8):
    """🏷️ 按标签筛选文章 - 必须在 /api/posts/{post_id} 之前注册！"""
    service = Get_Posts_By_Tag()
    result = service.get_posts_by_tag(tag_name=tag_name, page=page, page_size=size)
    return result


class Get_Posts_Filter:
    @staticmethod
    def _parse_tags(raw_tags):
        if isinstance(raw_tags, list):
            return [str(t).strip().strip('"\'') for t in raw_tags]
        if not isinstance(raw_tags, str) or not raw_tags.strip():
            return []
        stripped = raw_tags.strip()
        if (stripped.startswith('[') and stripped.endswith(']')) or \
           (stripped.startswith('{') and stripped.endswith('}')):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return [str(t).strip().strip('"\'') for t in parsed if t]
                return [str(parsed).strip()]
            except (json.JSONDecodeError, TypeError):
                pass
        import re
        parts = re.split(r'[,;，；|\/\\]+', stripped)
        return [p.strip().strip('"\'') for p in parts if p.strip()]

    def get_filtered_posts(self, tag_names: list[str] | None = None, category: str | None = None, page=1, page_size=8):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                conditions = ["visibility = 'public'"]
                params: list = []
                if category and category != 'all':
                    cursor.execute("SELECT id FROM categories WHERE slug = ? OR name = ? OR id = ?", (category, category, category))
                    cat_row = cursor.fetchone()
                    if cat_row:
                        conditions.append("category_id = ?")
                        params.append(cat_row['id'])
                    else:
                        return {"code": 200, "msg": "success", "total": 0, "page": page, "page_size": page_size, "data": []}
                if tag_names and len(tag_names) > 0:
                    cursor.execute("SELECT id, tags FROM articles WHERE visibility = 'public' AND tags IS NOT NULL")
                    rows = cursor.fetchall()
                    matching_ids = set()
                    for row in rows:
                        article_tags = self._parse_tags(row['tags'])
                        clean_article_tags = {t.lower() for t in article_tags}
                        clean_tag_names = {t.strip().lower() for t in tag_names}
                        if clean_tag_names & clean_article_tags:
                            matching_ids.add(row['id'])
                    if not matching_ids:
                        return {"code": 200, "msg": "success", "total": 0, "page": page, "page_size": page_size, "data": []}
                    if params:
                        conditions.append(f"id IN ({','.join(['?']*len(matching_ids))})")
                        params.extend(matching_ids)
                    else:
                        conditions.append(f"id IN ({','.join(['?']*len(matching_ids))})")
                        params = list(matching_ids)
                where_clause = ' AND '.join(conditions)
                cursor.execute(f"SELECT COUNT(*) as count FROM articles WHERE {where_clause}", params)
                total = cursor.fetchone()['count']
                offset = (page - 1) * page_size
                query = (
                    f"SELECT id, author_id as user_id, title, content, "
                    f"content_format as content_type, summary, cover_img, "
                    f"tags, status, visibility, is_top, "
                    f"publish_time as created_at, update_time as updated_at "
                    f"FROM articles WHERE {where_clause} "
                    f"ORDER BY is_top DESC, update_time DESC LIMIT ? OFFSET ?"
                )
                cursor.execute(query, [*params, page_size, offset])
                data = dicts_from_rows(cursor.fetchall())
                return {"code": 200, "msg": "success", "total": total, "page": page, "page_size": page_size, "data": data}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"code": 500, "msg": f"Server Error: {str(e)}", "data": []}


@app.get("/api/posts/filter")
async def get_filtered_posts_api(
    tags: str | None = None,
    category: str | None = None,
    page: int = 1,
    size: int = 8
):
    """🔗 组合筛选文章（支持多标签 + 分类）- 必须在 /api/posts/{post_id} 之前注册！"""
    tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else None
    service = Get_Posts_Filter()
    result = service.get_filtered_posts(
        tag_names=tag_list, category=category, page=page, page_size=size
    )
    return result


@app.get("/api/posts/{post_id}", response_model=APIResponse)
async def get_post_detail(post_id: int):
    service = Get_Post()
    result = service.get_post(post_id)
    if result["code"] == 404:
        raise HTTPException(status_code=404, detail=result["msg"])
    return result


@app.put("/api/posts/{post_id}", response_model=APIResponse)
async def update_post_detail(post_id: int, update_data: UpdatePostRequest = Body(...), _: bool = Depends(verify_api_key)):
    service = Update_Post()
    result = service.update_post(post_id=post_id, **update_data.dict(exclude_unset=True))
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["msg"])
    return result


@app.delete("/api/posts/{post_id}", response_model=APIResponse)
async def delete_post_detail(post_id: int, _: bool = Depends(verify_api_key)):
    service = Delete_Post()
    result = service.delete_post(post_id)
    return result

@app.get("/api/data_count", response_model=APIResponse)
async def data_count_post():
    """📊 获取全站数据统计"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 1️⃣ 公开文章总数
            cursor.execute("SELECT COUNT(*) as count FROM articles WHERE visibility = 'public'")
            texts_count = cursor.fetchone()["count"]

            # 2️⃣ 总阅读量 (需确保 articles 表存在 views 字段)
            cursor.execute("SELECT COALESCE(SUM(views), 0) as total_views FROM articles WHERE visibility = 'public'")
            read_count = cursor.fetchone()["total_views"] or 0

            # 3️⃣ 独立访客数 (UV) - 基于 IP 去重统计
        
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS site_visits (
                        ip_address TEXT PRIMARY KEY,
                        visit_count INTEGER DEFAULT 1,
                        last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            conn.commit()

            cursor.execute("SELECT COUNT(*) as uv FROM site_visits")
            customer_count = cursor.fetchone()["uv"] or 0

            return {
                "code": 200,
                "msg": "success",
                "data": {
                    "texts_count": texts_count,
                    "read_count": read_count,
                    "customer_count": customer_count
                }
            }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"code": 500, "msg": f"Server Error: {str(e)}", "data": None}


@app.get("/api/categories", response_model=APIResponse)
async def get_categories_list():
    """📁 获取全部分类列表"""
    service = Get_Categories()
    result = service.get_categories()
    return result


@app.get("/api/tags", response_model=APIResponse)
async def get_tags_list():
    """🏷️ 获取全部标签列表"""
    service = Get_Tags()
    result = service.get_tags()
    return result


@app.get("/api/resources", response_model=APIResponse)
async def get_resources_list():
    """🔐 获取资源列表"""
    service = Get_Resources()
    result = service.get_resources()
    return result


class VerifyPasswordRequest(BaseModel):
    resource_id: int
    password: str


@app.post("/api/resources/verify", response_model=APIResponse)
async def verify_resource_password_api(request_data: VerifyPasswordRequest):
    """🔑 验证资源访问密码"""
    service = Verify_Resource_Password()
    result = service.verify_password(resource_id=request_data.resource_id, password=request_data.password)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["msg"])
    return result


@app.get("/api/profile", response_model=APIResponse)
async def get_profile_info():
    """👤 获取个人资料信息"""
    service = Get_Profile()
    result = service.get_profile()
    return result


# --- 邮箱订阅 ---

import re
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class SubscribeRequest(BaseModel):
    email: str

@app.post("/api/subscribe", response_model=APIResponse)
async def subscribe_email(request: SubscribeRequest, ip: str = Depends(get_client_ip)):
    """📧 订阅邮箱 — 接收邮箱地址并保存到数据库"""
    email = request.email.strip().lower()
    
    if not EMAIL_PATTERN.match(email):
        return {"code": 400, "msg": "邮箱格式不正确", "data": None}
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 检查是否已订阅
            cursor.execute("SELECT id, status FROM subscriptions WHERE email = ?", (email,))
            existing = cursor.fetchone()
            if existing and existing["status"] == "active":
                return {"code": 409, "msg": "该邮箱已订阅", "data": None}
            elif existing and existing["status"] == "unsubscribed":
                # 重新激活
                cursor.execute(
                    "UPDATE subscriptions SET status = 'active', subscribed_at = CURRENT_TIMESTAMP WHERE email = ?",
                    (email,)
                )
            else:
                cursor.execute(
                    "INSERT INTO subscriptions (email, ip_address) VALUES (?, ?)",
                    (email, ip)
                )
            conn.commit()
        return {"code": 200, "msg": "订阅成功，感谢您的关注！", "data": {"email": email}}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"code": 500, "msg": f"服务器错误: {str(e)}", "data": None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)