<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { get_data_count, get_texts, type Data_count, type PostItem } from '@/api/api'
import { normalizeTags, truncateText, getRelativeTime } from '@/utils/index'

// ==================== 粒子配置 ====================
const PARTICLE_COUNT = 50
const particles = Array.from({ length: PARTICLE_COUNT }).map((_, i) => ({
  id: i,
  left: `${Math.random() * 100}%`,
  top: `${Math.random() * 100}%`,
  delay: `${Math.random() * 5}s`,
  duration: `${4 + Math.random() * 4}s`,
  size: `${2 + Math.random() * 3}px`
}))

// ==================== 波浪路径 ====================
const wavePaths = [
  "M0,64 C480,150 720,0 1200,64 L1200,120 L0,120 Z",
  "M0,80 C300,10 900,110 1200,80 L1200,120 L0,120 Z",
  "M0,100 C600,140 800,60 1200,100 L1200,120 L0,120 Z"
]

// ==================== 路由 ====================
const router = useRouter()
const isScrolled = ref(false)

// ==================== 数据统计状态 ====================
const stats = ref<Data_count | null>(null)
const statsLoading = ref(true)

// ==================== 文章列表状态 ====================
const recentPosts = ref<PostItem[]>([])
const postsLoading = ref(true)

// ==================== 处理后的文章数据 ====================
const processedPosts = computed(() => {
  return recentPosts.value.slice(0, 3).map(post => ({
    id: post.id,
    title: post.title,
    summary: post.summary || truncateText(post.content, 100),
    tags: normalizeTags(post.tags),
    date: getRelativeTime(post.created_at)
  }))
})

// ==================== 获取统计数据 ====================
const fetchStats = async () => {
  try {
    const res = await get_data_count()
    if (res.code === 200) {
      stats.value = res.data
    }
  } catch (err) {
    console.error('📊 获取统计数据失败:', err)
    stats.value = { texts_count: 0, read_count: 0, customer_count: 0 }
  } finally {
    statsLoading.value = false
  }
}

// ==================== 获取最新文章 ====================
const fetchRecentPosts = async () => {
  try {
    const res = await get_texts(1, 5)
    if (res.code === 200) {
      recentPosts.value = res.data || []
    }
  } catch (err) {
    console.error('📝 获取文章列表失败:', err)
    recentPosts.value = []
  } finally {
    postsLoading.value = false
  }
}

// ==================== 滚动监听 ====================
const handleScroll = () => {
  isScrolled.value = window.scrollY > 100
}

// ==================== 导航跳转 ====================
const navigateTo = (path: string) => {
  router.push(path)
}

// ==================== 数字格式化 ====================
const formatNumber = (num: number): string => {
  if (num >= 10000) return (num / 10000).toFixed(1) + 'w'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'k'
  return String(num)
}

// ==================== 生命周期 ====================
onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
  fetchStats()
  fetchRecentPosts()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="home-page">
    <!-- 页面背景层 -->
    <div class="page-background"></div>

    <!-- Hero 区域 -->
    <section class="hero-section" :class="{ 'scrolled': isScrolled }">

      <!-- 背景特效 -->
      <div class="hero-bg-effects">
        <div class="gradient-orb orb-1"></div>
        <div class="gradient-orb orb-2"></div>
        <div class="gradient-orb orb-3"></div>
        <div class="grid-overlay"></div>
      </div>

      <!-- 粒子层 -->
      <div class="hero-particles">
        <div
            v-for="p in particles"
            :key="p.id"
            class="particle"
            :style="{
              left: p.left,
              top: p.top,
              animationDelay: p.delay,
              animationDuration: p.duration,
              width: p.size,
              height: p.size
            }"
        ></div>
      </div>

      <!-- 主内容 -->
      <div class="hero-content">
        <div class="hero-badge fade-in-up" style="animation-delay: 0.1s">
          <span class="badge-dot"></span>
          欢迎来到我的博客
        </div>

        <h1 class="hero-title fade-in-up" style="animation-delay: 0.2s">
          <span class="title-line">探索技术的</span>
          <span class="title-gradient">无限可能</span>
        </h1>

        <p class="hero-subtitle fade-in-up" style="animation-delay: 0.3s">
          记录成长轨迹，分享技术心得，与志同道合者同行
        </p>

        <!-- 🔹 动态统计区域 -->
        <div class="hero-stats fade-in-up" style="animation-delay: 0.4s">
          <!-- 文章数 -->
          <div class="stat-item">
            <span class="stat-number">
              <span v-if="statsLoading" class="stat-skeleton">---</span>
              <span v-else>{{ formatNumber(stats?.texts_count ?? 0) }}</span>
            </span>
            <span class="stat-label">篇文章</span>
          </div>

          <div class="stat-divider"></div>

          <!-- 阅读量 -->
          <div class="stat-item">
            <span class="stat-number">
              <span v-if="statsLoading" class="stat-skeleton">---</span>
              <span v-else>{{ formatNumber(stats?.read_count ?? 0) }}</span>
            </span>
            <span class="stat-label">阅读量</span>
          </div>

          <div class="stat-divider"></div>

          <!-- 访客数 -->
          <div class="stat-item">
            <span class="stat-number">
              <span v-if="statsLoading" class="stat-skeleton">---</span>
              <span v-else>{{ formatNumber(stats?.customer_count ?? 0) }}</span>
            </span>
            <span class="stat-label">访客</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="hero-actions fade-in-up" style="animation-delay: 0.5s">
          <button class="hero-btn primary" @click="navigateTo('/posts')">
            <span class="btn-content">
              <span class="btn-text">开始阅读</span>
              <svg class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </span>
            <span class="btn-glow"></span>
          </button>
          <button class="hero-btn secondary" @click="navigateTo('/about')">
            <span class="btn-text">了解更多</span>
          </button>
        </div>
      </div>

      <!-- 波浪过渡层 -->
      <div class="hero-wave-container">
        <svg class="wave-svg wave-1" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path :d="wavePaths[0]" fill="rgba(217, 119, 6, 0.1)"></path>
        </svg>
        <svg class="wave-svg wave-2" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path :d="wavePaths[1]" fill="rgba(180, 83, 9, 0.08)"></path>
        </svg>
        <svg class="wave-svg wave-3" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path :d="wavePaths[2]" fill="rgba(245, 158, 11, 0.05)"></path>
        </svg>
      </div>
    </section>

    <!-- 内容区域 (波浪下方) -->
    <main class="content-section">
      <div class="content-container">
        <!-- 最新文章标题 -->
        <div class="section-header">
          <h2 class="section-title">最新文章</h2>
          <button class="view-all-btn" @click="navigateTo('/posts')">
            查看全部 <svg class="arrow-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
        </div>

        <!-- 文章卡片列表 -->
        <div class="articles-grid" v-if="!postsLoading">
          <div
              v-for="(post, index) in processedPosts"
              :key="post.id"
              class="article-card"
              :style="{ animationDelay: `${index * 0.15}s` }"
              @click="navigateTo(`/posts/${post.id}`)"
          >
            <div class="card-tags">
              <span v-for="tag in post.tags.slice(0, 2)" :key="tag" class="card-tag">{{ tag }}</span>
            </div>
            <h3 class="card-title">{{ post.title }}</h3>
            <p class="card-summary">{{ post.summary }}</p>
            <div class="card-footer">
              <span class="card-date">{{ post.date }}</span>
              <span class="read-more">阅读全文 →</span>
            </div>
          </div>

          <div v-if="processedPosts.length === 0" class="empty-state">
            <div class="empty-icon">📝</div>
            <p>暂无发布文章</p>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-else class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* ===== 页面级变量 ===== */
.home-page {
  --primary-color: #d97706;
  --secondary-color: #b45309;
  --accent-color: #f59e0b;
  --text-primary: #451a03;
  --text-secondary: #78350f;
  --text-muted: #92400e;
  --bg-page: #FFFBEB;
  --bg-content: #FEFCE8;
  --border-light: rgba(180, 83, 9, 0.15);

  min-height: 100vh;
  background: var(--bg-page);
  overflow-x: hidden;
}

.page-background {
  position: fixed;
  inset: 0;
  background: linear-gradient(180deg, var(--bg-page) 0%, var(--bg-content) 100%);
  z-index: -2;
  pointer-events: none;
}

/* ===== Hero 区域 ===== */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding-top: 70px;
  transition: padding 0.3s ease;
}

.hero-section.scrolled {
  padding-top: 60px;
}

/* 背景特效 */
.hero-bg-effects {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: orbFloat 20s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.4) 0%, transparent 70%);
  top: -10%;
  left: -10%;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(249, 115, 22, 0.3) 0%, transparent 70%);
  bottom: -10%;
  right: -10%;
  animation-delay: -5s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(234, 88, 12, 0.25) 0%, transparent 70%);
  top: 40%;
  left: 40%;
  animation-delay: -10s;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
      linear-gradient(rgba(180, 83, 9, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(180, 83, 9, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 20%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 20%, transparent 70%);
}

/* 粒子效果 */
.hero-particles {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: var(--primary-color);
  border-radius: 50%;
  opacity: 0;
  box-shadow: 0 0 10px rgba(217, 119, 6, 0.5);
  animation: particleRise linear infinite;
  will-change: transform, opacity;
}

@keyframes particleRise {
  0% { opacity: 0; transform: translateY(0) scale(0); }
  20% { opacity: 0.8; transform: translateY(-20px) scale(1); }
  80% { opacity: 0.5; }
  100% { opacity: 0; transform: translateY(-100px) scale(0.5); }
}

/* 骨架屏加载动画 */
.stat-skeleton {
  display: inline-block;
  width: 2.5rem;
  height: 1.5rem;
  background: linear-gradient(90deg,
  rgba(217, 119, 6, 0.1) 25%,
  rgba(217, 119, 6, 0.2) 50%,
  rgba(217, 119, 6, 0.1) 75%);
  background-size: 200% 100%;
  animation: skeletonLoad 1.5s infinite;
  border-radius: 4px;
  vertical-align: middle;
}

@keyframes skeletonLoad {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 数字悬停反馈 */
.stat-number {
  transition: transform 0.2s ease;
}
.stat-number:not(.stat-skeleton):hover {
  transform: scale(1.05);
}

/* 内容层 */
.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 800px;
  padding: 0 1.5rem;
  color: var(--text-primary);
}

.fade-in-up {
  opacity: 0;
  animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(251, 191, 36, 0.2);
  border: 1px solid rgba(217, 119, 6, 0.3);
  border-radius: 9999px;
  color: var(--secondary-color);
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  backdrop-filter: blur(4px);
}

.badge-dot {
  width: 6px;
  height: 6px;
  background: var(--primary-color);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--primary-color);
  animation: pulseDot 2s infinite;
}

@keyframes pulseDot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.title-line {
  display: block;
}

.title-gradient {
  display: block;
  background: linear-gradient(135deg, #d97706, #ea580c, #ca8a04);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% auto;
  animation: gradientText 5s ease infinite;
}

@keyframes gradientText {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto 2.5rem;
}

.hero-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2.5rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 80px;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.stat-divider {
  width: 1px;
  height: 2rem;
  background: rgba(180, 83, 9, 0.2);
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.hero-btn {
  position: relative;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  overflow: hidden;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
}

.hero-btn.primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  box-shadow: 0 4px 15px rgba(217, 119, 6, 0.3);
}

.hero-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(217, 119, 6, 0.4);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  z-index: 1;
}

.btn-arrow {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.hero-btn.primary:hover .btn-arrow {
  transform: translateX(4px);
}

.hero-btn.secondary {
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(180, 83, 9, 0.2);
  color: var(--text-secondary);
  backdrop-filter: blur(4px);
}

.hero-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.8);
  color: var(--primary-color);
  border-color: var(--primary-color);
}

/* 波浪层 */
.hero-wave-container {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 120px;
  z-index: 5;
  overflow: hidden;
}

.wave-svg {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: 100%;
}

.wave-1 { animation: waveMove 15s linear infinite; opacity: 0.8; }
.wave-2 { animation: waveMove 20s linear infinite reverse; opacity: 0.6; bottom: 10px; }
.wave-3 { animation: waveMove 25s linear infinite; opacity: 0.4; bottom: 20px; }

@keyframes waveMove {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* 滚动指示器 */
.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  z-index: 10;
  cursor: pointer;
  user-select: none;
}

.mouse {
  width: 24px;
  height: 36px;
  border: 2px solid rgba(180, 83, 9, 0.3);
  border-radius: 12px;
  display: flex;
  justify-content: center;
  padding-top: 6px;
}

.wheel {
  width: 4px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: scrollWheel 1.5s infinite;
}

@keyframes scrollWheel {
  0% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(12px); opacity: 0; }
}

.scroll-text {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* ===== 内容区域 ===== */
.content-section {
  position: relative;
  z-index: 20;
  background: var(--bg-content);
  padding: 4rem 0;
  margin-top: -60px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* 区域头部 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: none;
  border: 1px solid var(--border-light);
  border-radius: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.arrow-right {
  width: 1rem;
  height: 1rem;
  transition: transform 0.2s ease;
}

.view-all-btn:hover .arrow-right {
  transform: translateX(4px);
}

/* 文章卡片网格 */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

/* 文章卡片 */
.article-card {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--border-light);
  border-radius: 1rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUpCard 0.6s ease forwards;
  backdrop-filter: blur(8px);
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(139, 69, 19, 0.1);
  border-color: var(--primary-color);
}

@keyframes fadeInUpCard {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.card-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.card-tag {
  padding: 0.25rem 0.6rem;
  background: rgba(217, 119, 6, 0.1);
  color: var(--secondary-color);
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 9999px;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-summary {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-date {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.read-more {
  font-size: 0.85rem;
  color: var(--primary-color);
  font-weight: 500;
  transition: color 0.2s ease;
}

.article-card:hover .read-more {
  color: var(--secondary-color);
}

/* 空状态 */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid var(--border-light);
  border-radius: 1rem;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state p {
  color: var(--text-muted);
  font-size: 1rem;
}

/* 加载状态 */
.loading-container {
  text-align: center;
  padding: 4rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(217, 119, 6, 0.2);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== 响应式适配 ===== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-stats {
    gap: 1rem;
    flex-wrap: wrap;
  }

  .stat-number {
    font-size: 1.25rem;
  }

  .hero-actions {
    flex-direction: column;
    width: 100%;
    padding: 0 1rem;
  }

  .hero-btn {
    width: 100%;
    justify-content: center;
  }

  .scroll-indicator {
    display: none;
  }

  .content-section {
    margin-top: -40px;
    padding: 3rem 0;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .articles-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .article-card {
    padding: 1.25rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .hero-badge {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
  }

  /* 移动端统计项横向紧凑排列 */
  .hero-stats {
    gap: 0.5rem;
  }
  .stat-divider {
    display: none;
  }
  .stat-item {
    flex-direction: row;
    gap: 0.25rem;
    min-width: auto;
  }
  .stat-number {
    font-size: 1.1rem;
  }
  .stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
}
</style>