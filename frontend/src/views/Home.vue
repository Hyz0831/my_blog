<script setup lang="ts">
import { ref, shallowRef, onMounted, computed, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ArrowRight, Document, TrendCharts, ChatLineRound, 
  Collection, Search, Calendar
} from '@element-plus/icons-vue'
import { get_data_count, get_texts } from '../api/api'
import type { PostItem, Data_count } from '../api/api'
import { normalizeTags, getRelativeTime } from '../utils/index'

const router = useRouter()
const isLoaded = ref(false)
const isLoading = ref(true)

// 从 API 获取的数据
const stats = shallowRef<{ icon: any; value: string; label: string }[]>([])
const recentPosts = ref<PostItem[]>([])
const categories = ['前端架构', '后端开发', 'DevOps', 'UI/UX', '技术随笔', '开源贡献']

// 处理后的文章数据
const processedPosts = computed(() => {
  return recentPosts.value.slice(0, 3).map(post => ({
    id: post.id,
    title: post.title,
    date: getRelativeTime(post.created_at),
    tag: normalizeTags(post.tags)[0] || '未分类'
  }))
})

// 加载数据
const loadData = async () => {
  isLoading.value = true
  try {
    // 并行获取统计数据和文章列表
    const [countResult, postsResult] = await Promise.all([
      get_data_count(),
      get_texts(1, 5)
    ])

    const countData = countResult.data as Data_count
    stats.value = [
      { icon: markRaw(Document), value: countData.texts_count.toString(), label: '篇原创' },
      { icon: markRaw(TrendCharts), value: countData.read_count >= 1000 ? `${(countData.read_count / 1000).toFixed(1)}k` : countData.read_count.toString(), label: '次阅读' },
      { icon: markRaw(ChatLineRound), value: countData.customer_count.toString(), label: '位访客' },
    ]

    recentPosts.value = postsResult.data || []
  } catch (error) {
    console.error('数据加载失败:', error)
    // 使用备用数据
    stats.value = [
      { icon: markRaw(Document), value: '10', label: '篇原创' },
      { icon: markRaw(TrendCharts), value: '17', label: '次阅读' },
      { icon: markRaw(ChatLineRound), value: '1', label: '位访客' },
    ]
    recentPosts.value = [
      { id: 1, title: '欢迎访问我的博客', created_at: new Date().toISOString(), tags: ['欢迎'] } as PostItem
    ]
  } finally {
    isLoading.value = false
    setTimeout(() => isLoaded.value = true, 100)
  }
}

// 触发入场动画
onMounted(() => {
  loadData()
})

const navigate = (path: string) => router.push(path)
</script>

<!-- 脚本部分保持不变，仅修改模板和样式 -->
<template>
  <div class="home-bento">
    <!-- 动态背景层 -->
    <div class="bg-gradient"></div>
    <div class="bg-noise"></div>

    <main class="bento-container">
      <div class="bento-grid">
        
        <!-- 1. 个人介绍区 -->
        <div class="bento-card hero" :class="{ 'animate-in': isLoaded }">
          <div class="hero-content">
            <div class="avatar-wrapper">
              <span class="avatar-emoji">👨‍💻</span>
              <div class="status-dot"></div>
            </div>
            <h1 class="hero-title">你好，我是<span class="highlight">Kang</span></h1>
            <p class="hero-desc">aaaaaaaaa<br>在这里记录代码、思考与生活。</p>
            <div class="hero-actions">
              <button class="btn btn-primary" @click="navigate('/about')">了解更多</button>
              <button class="btn btn-ghost" @click="navigate('/posts')">浏览文章</button>
            </div>
          </div>
        </div>

        <!-- 2. 数据统计 -->
        <div class="bento-card stats" :class="{ 'animate-in': isLoaded }">
          <div v-for="(s, i) in stats" :key="i" class="stat-item">
            <div class="stat-icon">
              <el-icon><component :is="s.icon" /></el-icon>
            </div>
            <div class="stat-data">
              <span class="num">{{ s.value }}</span>
              <span class="label">{{ s.label }}</span>
            </div>
          </div>
        </div>

        <!-- 3. 最近更新 -->
        <div class="bento-card posts" :class="{ 'animate-in': isLoaded }">
          <div class="card-header">
            <h2><el-icon><Calendar /></el-icon> 最近更新</h2>
            <button class="link-arrow" @click="navigate('/posts')">查看全部 <el-icon><ArrowRight /></el-icon></button>
          </div>
          <div class="post-list">
            <div v-for="post in processedPosts" :key="post.id" class="post-row" @click="navigate(`/posts/${post.id}`)">
              <span class="post-tag">{{ post.tag }}</span>
              <div class="post-meta">
                <h3>{{ post.title }}</h3>
                <span class="post-date">{{ post.date }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. 分类导航 -->
        <div class="bento-card categories" :class="{ 'animate-in': isLoaded }">
          <h2><el-icon><Search /></el-icon> 内容分类</h2>
          <div class="tag-grid">
            <span v-for="cat in categories" :key="cat" class="tag-chip" @click="navigate(`/posts?cat=${cat}`)">
              {{ cat }}
            </span>
          </div>
          <div class="deco-shape">✨</div>
        </div>

        <!-- 5. 订阅引导 (通栏) -->
        <div class="bento-card subscribe" :class="{ 'animate-in': isLoaded }">
          <div class="sub-inner">
            <div class="sub-icon">
              <el-icon><Collection /></el-icon>
            </div>
            <div class="sub-text">
              <h2>保持连接，不错过更新</h2>
              <p>每周精选技术干货直达邮箱，无广告，随时退订。</p>
            </div>
            <div class="sub-form">
              <input type="email" placeholder="your@email.com" />
              <button class="btn btn-primary">立即订阅</button>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped>
/* ===== 暖色设计系统 ===== */
.home-bento {
  --nav-height: 70px; /* 与导航栏高度保持一致 */
  --safe-top: calc(var(--nav-height) + 1.5rem); /* 安全间距：导航栏高度 + 额外留白 */
  
  --warm-50: #FFFBEB;
  --warm-100: #FEF3C7;
  --warm-500: #F59E0B;
  --warm-600: #D97706;
  --warm-700: #B45309;
  --warm-800: #92400E;
  --warm-900: #78350F;
  --warm-950: #451A03;
  
  --glass: rgba(254, 243, 199, 0.55);
  --glass-hover: rgba(254, 243, 199, 0.8);
  --border: rgba(180, 83, 9, 0.12);
  --border-hover: rgba(217, 119, 6, 0.35);
  
  --shadow: 0 4px 20px rgba(139, 69, 19, 0.06);
  --shadow-hover: 0 10px 30px rgba(139, 69, 19, 0.1);
  
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  
  min-height: 100vh;
  position: relative;
  /* ✅ 核心修复：添加顶部 padding，避免被固定导航栏遮挡 */
  padding: var(--safe-top) 1rem 4rem;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans SC", sans-serif;
  color: var(--warm-950);
  overflow-x: hidden;
}

/* 背景层 */
.bg-gradient {
  position: fixed; inset: 0; z-index: -2;
  background: radial-gradient(circle at 15% 20%, rgba(245, 158, 11, 0.15) 0%, transparent 40%),
              radial-gradient(circle at 85% 80%, rgba(180, 83, 9, 0.12) 0%, transparent 40%),
              linear-gradient(180deg, var(--warm-50) 0%, var(--warm-100) 100%);
}
.bg-noise {
  position: fixed; inset: 0; z-index: -1; opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  pointer-events: none;
}

.bento-container { max-width: 1280px; margin: 0 auto; }

/* ===== Bento Grid 布局 ===== */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  gap: 1.25rem;
}

/* 卡片通用样式 */
.bento-card {
  background: var(--glass);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  border-radius: 1.25rem;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  transition: all 0.35s var(--ease);
  position: relative;
  overflow: hidden;
  opacity: 0; transform: translateY(20px);
}

.bento-card.animate-in {
  opacity: 1; transform: translateY(0);
  transition: opacity 0.6s var(--ease), transform 0.6s var(--ease);
}

.bento-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
  border-color: var(--border-hover);
  background: var(--glass-hover);
}

/* 网格位置分配 */
.hero   { grid-column: span 2; grid-row: span 2; display: flex; align-items: center; }
.stats  { grid-column: span 1; grid-row: span 1; }
.posts  { grid-column: span 2; grid-row: span 1; }
.categories { grid-column: span 1; grid-row: span 1; }
.subscribe { grid-column: span 4; grid-row: span 1; }

/* ===== 1. Hero 区域 ===== */
.hero-content { width: 100%; }
.avatar-wrapper {
  width: 64px; height: 64px; position: relative; margin-bottom: 1.25rem;
}
.avatar-emoji {
  width: 100%; height: 100%; background: var(--warm-100); border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-size: 2rem;
  border: 2px solid var(--warm-500);
}
.status-dot {
  position: absolute; bottom: 2px; right: 2px; width: 14px; height: 14px;
  background: #22c55e; border: 2px solid var(--warm-50); border-radius: 50%;
}
.hero-title {
  font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; line-height: 1.2; margin-bottom: 0.75rem;
}
.highlight {
  background: linear-gradient(135deg, var(--warm-600), var(--warm-500));
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-desc { color: var(--warm-800); line-height: 1.6; margin-bottom: 1.5rem; }
.hero-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.btn {
  padding: 0.65rem 1.25rem; border-radius: 0.75rem; font-weight: 600; cursor: pointer;
  transition: all 0.25s var(--ease); border: none; font-size: 0.95rem;
}
.btn-primary {
  background: linear-gradient(135deg, var(--warm-600), var(--warm-500)); color: white;
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(217, 119, 6, 0.4); }
.btn-ghost {
  background: transparent; color: var(--warm-700); border: 1px solid var(--border);
}
.btn-ghost:hover { background: rgba(217, 119, 6, 0.08); border-color: var(--warm-600); }

/* ===== 2. 统计区 ===== */
.stats { display: flex; flex-direction: column; justify-content: center; gap: 1.25rem; }
.stat-item { display: flex; align-items: center; gap: 0.75rem; }
.stat-icon {
  width: 40px; height: 40px; background: rgba(217, 119, 6, 0.12); border-radius: 0.6rem;
  display: flex; align-items: center; justify-content: center; color: var(--warm-600);
}
.stat-data { display: flex; flex-direction: column; }
.stat-data .num { font-size: 1.25rem; font-weight: 700; color: var(--warm-950); }
.stat-data .label { font-size: 0.75rem; color: var(--warm-700); }

/* ===== 3. 文章列表 ===== */
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.card-header h2 { font-size: 1.1rem; font-weight: 600; color: var(--warm-900); display: flex; align-items: center; gap: 0.4rem; }
.link-arrow { background: none; border: none; color: var(--warm-600); cursor: pointer; font-size: 0.85rem; display: flex; align-items: center; gap: 0.3rem; }
.post-list { display: flex; flex-direction: column; gap: 0.75rem; }
.post-row {
  display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem; border-radius: 0.6rem; cursor: pointer; transition: background 0.2s;
}
.post-row:hover { background: rgba(217, 119, 6, 0.06); }
.post-tag {
  font-size: 0.7rem; padding: 0.2rem 0.5rem; background: rgba(217, 119, 6, 0.1); color: var(--warm-700);
  border-radius: 0.4rem; font-weight: 500; flex-shrink: 0;
}
.post-meta { flex: 1; min-width: 0; }
.post-meta h3 { font-size: 0.9rem; font-weight: 600; margin: 0 0 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.post-date { font-size: 0.75rem; color: var(--warm-700); }

/* ===== 4. 分类区 ===== */
.categories h2 { font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.4rem; }
.tag-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.tag-chip {
  padding: 0.4rem 0.8rem; background: rgba(255, 250, 235, 0.8); border: 1px solid var(--border);
  border-radius: 999px; font-size: 0.8rem; cursor: pointer; transition: all 0.2s;
}
.tag-chip:hover { background: var(--warm-600); color: white; border-color: var(--warm-600); transform: translateY(-2px); }
.deco-shape { position: absolute; bottom: 1rem; right: 1rem; font-size: 1.5rem; opacity: 0.3; transform: rotate(15deg); }

/* ===== 5. 订阅区 ===== */
.subscribe { background: linear-gradient(135deg, var(--warm-100), var(--warm-50)); border: 1px solid rgba(217, 119, 6, 0.2); }
.sub-inner { display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap; }
.sub-icon { width: 56px; height: 56px; background: var(--warm-600); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; flex-shrink: 0; }
.sub-text { flex: 1; min-width: 200px; }
.sub-text h2 { font-size: 1.25rem; font-weight: 700; margin: 0 0 0.3rem; }
.sub-text p { margin: 0; color: var(--warm-800); font-size: 0.9rem; }
.sub-form { display: flex; gap: 0.5rem; flex: 1; min-width: 250px; }
.sub-form input {
  flex: 1; padding: 0.7rem 1rem; border: 1px solid var(--border); border-radius: 0.75rem;
  background: white; color: var(--warm-950); outline: none; transition: all 0.2s;
}
.sub-form input:focus { border-color: var(--warm-600); box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.15); }

/* ===== 响应式适配 ===== */
@media (max-width: 1024px) {
  .bento-grid { grid-template-columns: repeat(2, 1fr); }
  .hero { grid-column: span 2; }
  .stats, .categories { grid-column: span 1; }
  .posts, .subscribe { grid-column: span 2; }
}

@media (max-width: 640px) {
  .home-bento { 
    /* ✅ 移动端适配：导航栏可能变矮，适当减小顶部间距 */
    padding: calc(60px + 1rem) 0.75rem 3rem; 
  }
  .bento-grid { grid-template-columns: 1fr; gap: 1rem; }
  .hero, .stats, .posts, .categories, .subscribe { grid-column: span 1; grid-row: auto; }
  .hero-content { text-align: center; }
  .hero-actions { justify-content: center; }
  .sub-inner { flex-direction: column; text-align: center; }
  .sub-form { width: 100%; flex-direction: column; }
  .sub-form input, .sub-form .btn { width: 100%; }
}
</style>