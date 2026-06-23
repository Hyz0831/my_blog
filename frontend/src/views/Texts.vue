<script setup lang="ts">
import { ref, shallowRef, onMounted, computed, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import bloglist from "../components/Bloglist.vue"
import { List, Reading, Clock, TrendCharts, Folder, PriceTag, Monitor, Cpu, SetUp, Brush, MagicStick } from '@element-plus/icons-vue'
import { get_data_count, get_texts, get_categories, get_tags, get_top_posts, subscribe_email } from '@/api/api.ts'
import type { Data_count, PostItem, CategoryItem, TagItem } from '@/api/api.ts'

const router = useRouter()
const isLoading = ref(true)
const stats = shallowRef<{ icon: any; label: string; value: string }[]>([])
const popularPosts = ref<PostItem[]>([])

const CATEGORY_ICON_MAP: Record<string, any> = {
  frontend: markRaw(Monitor),
  backend: markRaw(Cpu),
  devops: markRaw(SetUp),
  essay: markRaw(Brush),
  opensource: markRaw(MagicStick),
}

const categories = shallowRef<{ id: string; name: string; icon: any; count: number; active: boolean; color: string }[]>([
  { id: 'all', name: '全部文章', icon: markRaw(Folder), count: 0, active: true, color: '#d97706' },
])

const tags = ref<{ name: string; count: number; active: boolean; color: string; size: string }[]>([])

// --- 邮箱订阅 ---
const subEmail = ref('')
const subLoading = ref(false)
const subStatus = ref<'idle' | 'success' | 'error'>('idle')
const subMsg = ref('')

const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

const handleSubscribe = async () => {
  const email = subEmail.value.trim()
  if (!email) {
    subStatus.value = 'error'
    subMsg.value = '请输入邮箱地址'
    return
  }
  if (!EMAIL_REGEX.test(email)) {
    subStatus.value = 'error'
    subMsg.value = '邮箱格式不正确'
    return
  }

  subLoading.value = true
  subStatus.value = 'idle'
  try {
    const res = await subscribe_email(email)
    if (res.code === 200) {
      subStatus.value = 'success'
      subMsg.value = res.msg || '订阅成功！'
      subEmail.value = ''
      setTimeout(() => { subStatus.value = 'idle' }, 3000)
    } else if (res.code === 409) {
      subStatus.value = 'error'
      subMsg.value = res.msg || '该邮箱已订阅'
    } else {
      subStatus.value = 'error'
      subMsg.value = res.msg || '订阅失败'
    }
  } catch (e: any) {
    subStatus.value = 'error'
    subMsg.value = e.response?.data?.msg || '网络错误，请重试'
  } finally {
    subLoading.value = false
  }
}

interface TimeArchive {
  year: string
  months: { month: string; label: string; count: number }[]
  total: number
}

const timeArchives = ref<TimeArchive[]>([])

const activeCategory = ref('all')
const activeTags = ref<string[]>([])
const bloglistRef = ref<InstanceType<typeof bloglist> | null>(null)
const expandedYears = ref(new Set<string>())

const navigate = (path: string) => router.push(path)

const processedPopularPosts = computed(() => {
  return popularPosts.value.slice(0, 5).map((post, index) => ({
    rank: index + 1,
    id: post.id,
    title: post.title
  }))
})

const hasActiveFilter = computed(() => {
  return activeCategory.value !== 'all' || activeTags.value.length > 0
})

const currentFilterLabel = computed(() => {
  if (activeCategory.value !== 'all') {
    const cat = categories.value.find(c => c.id === activeCategory.value)
    return `📂 ${cat?.name || ''}`
  }
  if (activeTags.value.length > 0) {
    return `🏷️ ${activeTags.value.join(' + ')}`
  }
  return ''
})

const maxTagCount = computed(() => Math.max(...tags.value.map(t => t.count), 1))

const getCategoryPercentage = (cat: typeof categories.value[0]): string => {
  const total = categories.value[0]?.count || 1
  if (cat.id === 'all') return '100'
  return ((cat.count / total) * 100).toFixed(0)
}

const selectCategory = (categoryId: string) => {
  if (activeCategory.value === categoryId) return
  activeCategory.value = categoryId
  categories.value.forEach(cat => {
    cat.active = cat.id === categoryId
  })
  activeTags.value = []
  tags.value.forEach(tag => tag.active = false)
  applyFilter()
}

const toggleTag = (tagName: string) => {
  const index = activeTags.value.indexOf(tagName)
  if (index > -1) {
    activeTags.value.splice(index, 1)
  } else {
    activeTags.value.push(tagName)
  }
  tags.value.forEach(tag => {
    tag.active = activeTags.value.includes(tag.name)
  })
  if (activeTags.value.length > 0 && activeCategory.value !== 'all') {
    activeCategory.value = 'all'
    categories.value.forEach(cat => {
      cat.active = cat.id === 'all'
    })
  }
  applyFilter()
}

const clearAllFilters = () => {
  activeCategory.value = 'all'
  activeTags.value = []
  categories.value.forEach(cat => { cat.active = cat.id === 'all' })
  tags.value.forEach(tag => { tag.active = false })
  applyFilter()
}

const toggleArchiveYear = (year: string) => {
  if (expandedYears.value.has(year)) {
    expandedYears.value.delete(year)
  } else {
    expandedYears.value.add(year)
  }
}

const filterByTime = (year: string, month: string) => {
  console.log(`按时间筛选: ${year}-${month}`)
}

const applyFilter = () => {
  if (bloglistRef.value) {
    bloglistRef.value.setFilter({
      category: activeCategory.value,
      tags: [...activeTags.value]
    })
  }
}

const loadData = async () => {
  isLoading.value = true
  try {
    const [countResult, postsResult, categoriesResult, tagsResult, topPostsResult] = await Promise.all([
      get_data_count(),
      get_texts(1, 10),
      get_categories(),
      get_tags(),
      get_top_posts(5)
    ])

    const countData = countResult.data as Data_count
    const latestPost = postsResult.data?.[0]

    stats.value = [
      { icon: markRaw(Reading), label: '文章总数', value: countData.texts_count.toString() },
      { icon: markRaw(Clock), label: '更新时间', value: latestPost?.updated_at ? formatDate(latestPost.updated_at) : '暂无' },
      { icon: markRaw(TrendCharts), label: '阅读量', value: countData.read_count >= 1000 ? `${(countData.read_count / 1000).toFixed(1)}k` : countData.read_count.toString() },
    ]

    if (categoriesResult.data && Array.isArray(categoriesResult.data)) {
      const categoryColors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4']
      const apiCategories: { id: string; name: string; icon: any; count: number; active: boolean; color: string }[] = categoriesResult.data.map((cat: CategoryItem, idx: number) => ({
        id: cat.slug || cat.id.toString(),
        name: cat.name,
        icon: CATEGORY_ICON_MAP[cat.slug] || CATEGORY_ICON_MAP[cat.name.toLowerCase()] || markRaw(PriceTag),
        count: cat.count,
        active: false,
        color: categoryColors[idx % categoryColors.length] ?? '#6b7280'
      }))
      categories.value = [
        { id: 'all', name: '全部文章', icon: markRaw(Folder), count: countData.texts_count, active: true, color: '#d97706' },
        ...apiCategories
      ]
    }

    if (tagsResult.data && Array.isArray(tagsResult.data)) {
      const tagColors = ['#60a5fa', '#34d399', '#a78bfa', '#fbbf24', '#f87171', '#22d3ee', '#fb923c', '#c084fc']
      const rawTags = tagsResult.data.map((tag: TagItem, idx: number) => ({
        name: sanitizeTagName(tag.name),
        count: tag.count,
        active: false,
        color: tagColors[idx % tagColors.length] ?? '#9ca3af'
      })) as { name: string; count: number; active: boolean; color: string; size: string }[]
      const maxCount = Math.max(...rawTags.map(t => t.count), 1)
      tags.value = rawTags.map(tag => ({
        ...tag,
        size: tag.count >= maxCount * 0.8 ? 'lg' : tag.count >= maxCount * 0.4 ? 'md' : 'sm'
      }))
    }

    if (postsResult.data && Array.isArray(postsResult.data)) {
      const archiveMap = new Map<string, Map<string, number>>()
      postsResult.data.forEach((post: PostItem) => {
        if (!post.created_at) return
        const date = new Date(post.created_at.replace(' ', 'T'))
        if (isNaN(date.getTime())) return
        const year = date.getFullYear().toString()
        const month = `${date.getMonth() + 1}`.padStart(2, '0')
        const monthLabel = `${date.getMonth() + 1}月`
        if (!archiveMap.has(year)) archiveMap.set(year, new Map())
        const monthMap = archiveMap.get(year)!
        monthMap.set(month, (monthMap.get(month) || 0) + 1)
      })
      timeArchives.value = Array.from(archiveMap.entries())
        .sort((a, b) => Number(b[0]) - Number(a[0]))
        .map(([year, months]) => ({
          year,
          months: Array.from(months.entries())
            .sort((a, b) => Number(b[0]) - Number(a[0]))
            .map(([month, count]) => ({ month, label: `${Number(month)}月`, count })),
          total: Array.from(months.values()).reduce((s, c) => s + c, 0)
        }))
    }

    if (timeArchives.value.length > 0) {
      expandedYears.value.add(timeArchives.value[0].year)
    }

    popularPosts.value = topPostsResult.data || postsResult.data || []
  } catch (error) {
    console.error('数据加载失败:', error)
    stats.value = [
      { icon: markRaw(Reading), label: '文章总数', value: '0' },
      { icon: markRaw(Clock), label: '更新时间', value: '暂无' },
      { icon: markRaw(TrendCharts), label: '阅读量', value: '0' },
    ]
    categories.value = [{ id: 'all', name: '全部文章', icon: markRaw(Folder), count: 0, active: true, color: '#d97706' }]
    tags.value = []
    popularPosts.value = []
  } finally {
    isLoading.value = false
  }
}

const sanitizeTagName = (name: string): string => {
  if (!name) return ''
  return name.replace(/^['"\[\]]+|['"\[\]]+$/g, '').trim()
}

// 格式化日期
const formatDate = (dateStr: string): string => {
  if (!dateStr) return '暂无'
  const date = new Date(dateStr.replace(' ', 'T'))
  if (isNaN(date.getTime())) return '暂无'
  return `${date.getFullYear()}年${date.getMonth() + 1}月`
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div id="texts-page">
    <!-- 页面背景 -->
    <div class="page-background"></div>
    
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <List />
        </div>
        <div class="header-text">
          <h1 class="page-title">文章中心</h1>
          <p class="page-subtitle">探索技术文章与随笔，记录思考的点滴</p>
        </div>
      </div>
    </div>

    <div class="page-content">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div
            v-for="(stat, index) in stats"
            :key="stat.label"
            class="stat-card"
            :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <component :is="stat.icon" class="stat-icon" />
          <div class="stat-info">
            <p class="stat-value">{{ stat.value }}</p>
            <p class="stat-label">{{ stat.label }}</p>
          </div>
        </div>
      </div>

      <!-- 主内容布局 -->
      <div class="content-layout">
        <!-- 侧边栏 -->
        <aside class="sidebar">
          <div class="sidebar-section">
            <div class="section-header">
              <h3 class="section-title">📁 分类归档</h3>
              <button 
                v-if="activeCategory !== 'all'" 
                class="clear-tags-btn"
                @click="selectCategory('all')"
              >
                重置
              </button>
            </div>
            <nav class="category-nav">
              <button 
                v-for="category in categories" 
                :key="category.id"
                :class="['category-item', { active: category.active }]"
                :style="category.active ? { '--cat-color': category.color } : {}"
                @click="selectCategory(category.id)"
              >
                <component :is="category.icon" class="category-icon" />
                <div class="category-info">
                  <span class="category-name">{{ category.name }}</span>
                  <div v-if="category.id !== 'all' && categories[0]" class="category-progress">
                    <div 
                      class="category-progress-bar" 
                      :style="{ width: getCategoryPercentage(category) + '%', background: category.active ? category.color : 'var(--primary-color)' }"
                    ></div>
                  </div>
                </div>
                <span class="category-count" :style="category.active ? { background: category.color + '25', color: category.color } : {}">{{ category.count }}</span>
              </button>
            </nav>
          </div>

          <div class="sidebar-section">
            <div class="section-header">
              <h3 class="section-title">🏷️ 热门标签</h3>
              <button 
                v-if="activeTags.length > 0" 
                class="clear-tags-btn"
                @click="activeTags = []; tags.forEach(t => t.active = false)"
              >
                清除筛选
              </button>
            </div>
            <div class="tags-cloud">
              <span 
                v-for="tag in tags" 
                :key="tag.name"
                :class="['tag-item', `tag-${tag.size}`, { active: tag.active }]"
                :style="tag.active ? { '--tag-color': tag.color, borderColor: tag.color, background: tag.color + '18', color: tag.color } : {}"
                @click="toggleTag(tag.name)"
              >
                {{ tag.name }}
                <span class="tag-count">{{ tag.count }}</span>
              </span>
            </div>
          </div>

          <div class="sidebar-section">
            <h3 class="section-title">📅 时间归档</h3>
            <div v-if="timeArchives.length === 0" class="archive-empty">
              <span>暂无归档数据</span>
            </div>
            <div v-for="archive in timeArchives" :key="archive.year" class="archive-year-group">
              <div class="archive-year" @click="toggleArchiveYear(archive.year)">
                <svg class="archive-chevron" :class="{ expanded: expandedYears.has(archive.year) }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
                <span class="archive-year-label">{{ archive.year }} 年</span>
                <span class="archive-year-count">{{ archive.total }} 篇</span>
              </div>
              <transition name="archive-slide">
                <div v-show="expandedYears.has(archive.year)" class="archive-months">
                  <a
                    v-for="month in archive.months"
                    :key="month.month"
                    class="archive-month-item"
                    @click="filterByTime(archive.year, month.month)"
                  >
                    <span class="archive-month-label">{{ month.label }}</span>
                    <span class="archive-month-count">{{ month.count }}</span>
                  </a>
                </div>
              </transition>
            </div>
          </div>

          <div class="sidebar-section">
            <h3 class="section-title">📊 阅读排行</h3>
            <ol class="ranking-list">
              <li
                v-for="post in processedPopularPosts"
                :key="post.id"
                class="ranking-item"
                @click="navigate(`/posts/${post.id}`)"
              >
                <span class="rank-badge">{{ post.rank }}</span>
                <span class="rank-title">{{ post.title }}</span>
              </li>
              <li v-if="processedPopularPosts.length === 0" class="ranking-item empty">
                <span class="rank-title">暂无数据</span>
              </li>
            </ol>
          </div>

          <!-- 邮箱订阅 -->
          <div class="sidebar-section subscribe-card">
            <h3 class="section-title">📧 订阅更新</h3>
            <p class="subscribe-desc">第一时间获取最新文章推送</p>
            <form class="subscribe-form" @submit.prevent="handleSubscribe">
              <input
                v-model="subEmail"
                type="email"
                placeholder="your@email.com"
                :disabled="subLoading || subStatus === 'success'"
                class="subscribe-input"
              />
              <button
                type="submit"
                :class="['subscribe-btn', { loading: subLoading, success: subStatus === 'success' }]"
                :disabled="subLoading || subStatus === 'success'"
              >
                <template v-if="subLoading">
                  <svg class="spin-icon" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2.5" stroke-dasharray="31.4 31.4" stroke-linecap="round"/></svg>
                  提交中...
                </template>
                <template v-else-if="subStatus === 'success'">
                  ✓ 已订阅
                </template>
                <template v-else>订阅</template>
              </button>
            </form>
            <transition name="fade-slide">
              <p v-if="subMsg" :class="['subscribe-msg', subStatus]">{{ subMsg }}</p>
            </transition>
          </div>
        </aside>

        <!-- 主内容区 -->
        <main class="main-content">
          <div class="content-header">
            <div class="header-left">
              <h2 class="content-title">{{ hasActiveFilter ? currentFilterLabel : '最新文章' }}</h2>
              <span v-if="hasActiveFilter" class="filter-badge" @click="clearAllFilters">
                {{ activeCategory !== 'all' ? '分类' : '标签' }}筛选中
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
              </span>
            </div>
            <div class="header-right">
              <span class="content-count">{{ stats[0]?.value || '0' }} 篇文章</span>
              <button v-if="hasActiveFilter" class="clear-filter-btn" @click="clearAllFilters">
                清除全部
              </button>
            </div>
          </div>
          <bloglist ref="bloglistRef" @clear-filter="clearAllFilters" />
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ===== 暖色系变量定义 ===== */
#texts-page {
  --primary-color: #d97706;      /* Amber-600 */
  --secondary-color: #b45309;    /* Amber-700 */
  --accent-color: #f59e0b;       /* Amber-500 */
  
  --text-primary: #451a03;       /* Deep Brown */
  --text-secondary: #78350f;     /* Medium Brown */
  --text-muted: #92400e;         /* Light Brown */
  
  --bg-page: #FFFBEB;            /* Amber-50 */
  --bg-card: rgba(254, 243, 199, 0.6);  /* Amber-100 with opacity */
  --bg-card-solid: #FEF3C7;      /* Amber-100 solid */
  
  --border-light: rgba(180, 83, 9, 0.15);
  --border-hover: rgba(217, 119, 6, 0.4);
  
  --shadow-soft: 0 4px 20px rgba(139, 69, 19, 0.08);
  --shadow-hover: 0 12px 30px rgba(139, 69, 19, 0.12);
  
  --transition-fast: 0.2s ease;
  --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  min-height: 100vh;
  padding: 100px 1.5rem 4rem;
  position: relative;
  z-index: 1;
  background: var(--bg-page);
}

/* 页面背景渐变 */
.page-background {
  position: fixed;
  inset: 0;
  background: linear-gradient(180deg, var(--bg-page) 0%, #FEF9E7 100%);
  z-index: -1;
  pointer-events: none;
}

/* ===== 页面头部 ===== */
.page-header {
  margin-bottom: 3rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 暖色渐变图标背景 */
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  border-radius: 1rem;
  box-shadow: 0 8px 25px rgba(217, 119, 6, 0.3);
  flex-shrink: 0;
}

.header-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.header-text {
  flex: 1;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* ===== 统计卡片 ===== */
.page-content {
  max-width: 1400px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-light);
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all var(--transition-normal);
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

.stat-card:hover {
  transform: translateY(-3px);
  border-color: var(--border-hover);
  box-shadow: var(--shadow-hover);
  background: rgba(254, 243, 199, 0.8);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 暖色图标背景 */
  background: rgba(217, 119, 6, 0.15);
  border-radius: 0.75rem;
  color: var(--primary-color);
  font-size: 24px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 2px;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 500;
}

/* ===== 内容布局 ===== */
.content-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
}

.sidebar {
  position: sticky;
  top: 120px;
  height: fit-content;
  z-index: 10;
}

.sidebar-section {
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-light);
  border-radius: 1rem;
  padding: 1.25rem;
  margin-bottom: 1rem;
  transition: all var(--transition-normal);
}

.sidebar-section:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow-soft);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-light);
}

.section-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0;
}

.clear-tags-btn {
  font-size: 0.75rem;
  color: var(--primary-color);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  transition: all var(--transition-fast);
}

.clear-tags-btn:hover {
  background: rgba(217, 119, 6, 0.1);
}

/* 分类导航 */
.category-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-item {
  display: flex;
  align-items: center;
  text-align: left;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  transition: all var(--transition-fast);
  background: transparent;
  border: none;
  cursor: pointer;
  font-family: inherit;
  width: 100%;
  gap: 0.5rem;
}

.category-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.category-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.category-progress {
  height: 3px;
  background: rgba(180, 83, 9, 0.08);
  border-radius: 2px;
  overflow: hidden;
}

.category-progress-bar {
  height: 100%;
  border-radius: 2px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-name {
  flex: 1;
  text-align: left;
}

.category-count {
  font-size: 0.75rem;
  background: rgba(180, 83, 9, 0.1);
  color: var(--text-muted);
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-weight: 500;
}

.category-item:hover {
  background: rgba(217, 119, 6, 0.1);
  color: var(--primary-color);
}

.category-item:hover .category-count {
  background: rgba(217, 119, 6, 0.15);
  color: var(--primary-color);
}

.category-item.active {
  background: color-mix(in srgb, var(--cat-color, var(--primary-color)) 12%, transparent);
  color: var(--cat-color, var(--primary-color));
  font-weight: 600;
  border-left: 3px solid var(--cat-color, var(--primary-color));
  padding-left: calc(1rem - 3px);
}

.category-item.active .category-count {
  background: color-mix(in srgb, var(--cat-color, var(--primary-color)) 20%, transparent);
  color: var(--cat-color, var(--primary-color));
}

.category-item.active .category-icon {
  color: var(--cat-color, var(--primary-color));
}

/* 标签云 */
.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.3rem 0.65rem;
  background: rgba(217, 119, 6, 0.1);
  border: 1px solid rgba(217, 119, 6, 0.2);
  border-radius: 9999px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-weight: 500;
  line-height: 1.4;
}

.tag-sm { font-size: 0.7rem; }
.tag-md { font-size: 0.8rem; padding: 0.35rem 0.75rem; }
.tag-lg { font-size: 0.9rem; font-weight: 600; padding: 0.4rem 0.85rem; }

.tag-count {
  font-size: 0.625rem;
  opacity: 0.7;
}

.tag-item:hover {
  background: rgba(217, 119, 6, 0.2);
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(217, 119, 6, 0.15);
}

.tag-item.active {
  border-color: var(--tag-color, var(--primary-color));
  background: color-mix(in srgb, var(--tag-color, var(--primary-color)) 12%, transparent);
  color: var(--tag-color, var(--primary-color));
  font-weight: 700;
  box-shadow: 0 2px 10px color-mix(in srgb, var(--tag-color, var(--primary-color)) 15%, transparent);
}

.tag-item.active .tag-count {
  opacity: 1;
  color: var(--tag-color, var(--primary-color));
  font-weight: 600;
}

/* ===== 时间归档 ===== */
.archive-empty {
  text-align: center;
  padding: 1.5rem 0;
  color: var(--text-muted);
  font-size: 0.8rem;
}

.archive-year-group {
  margin-bottom: 0.5rem;
}

.archive-year-group:last-child {
  margin-bottom: 0;
}

.archive-year {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all var(--transition-fast);
  user-select: none;
}

.archive-year:hover {
  background: rgba(217, 119, 6, 0.08);
}

.archive-chevron {
  width: 14px;
  height: 14px;
  color: var(--text-muted);
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.archive-chevron.expanded {
  transform: rotate(180deg);
}

.archive-year-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}

.archive-year-count {
  font-size: 0.7rem;
  color: var(--text-muted);
  background: rgba(180, 83, 9, 0.08);
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  margin-left: auto;
}

.archive-months {
  padding-left: 1.7rem;
  overflow: hidden;
}

.archive-month-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.35rem 0.6rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.archive-month-item:hover {
  background: rgba(217, 119, 6, 0.1);
  color: var(--primary-color);
  transform: translateX(4px);
}

.archive-month-label {
  font-weight: 500;
}

.archive-month-count {
  font-size: 0.7rem;
  color: var(--text-muted);
  min-width: 20px;
  text-align: right;
}

/* Archive slide transition */
.archive-slide-enter-active,
.archive-slide-leave-active {
  transition: all 0.35s ease;
  overflow: hidden;
}

.archive-slide-enter-from,
.archive-slide-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-8px);
}

.archive-slide-enter-to,
.archive-slide-leave-from {
  opacity: 1;
  max-height: 400px;
  transform: translateY(0);
}

/* 阅读排行 */
.ranking-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.ranking-item:last-child {
  border-bottom: none;
}

.ranking-item:hover {
  transform: translateX(5px);
}

.ranking-item:hover .rank-title {
  color: var(--primary-color);
}

.rank-badge {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(217, 119, 6, 0.15);
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--primary-color);
  flex-shrink: 0;
}

.rank-title {
  flex: 1;
  font-size: 0.875rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color var(--transition-fast);
}

/* ===== 邮箱订阅 ===== */
.subscribe-card {
  background: linear-gradient(135deg, rgba(217, 119, 6, 0.08), rgba(251, 191, 36, 0.06));
  border-color: rgba(217, 119, 6, 0.2) !important;
}
.subscribe-desc {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin: -0.5rem 0 0.75rem;
}

.subscribe-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.subscribe-input {
  width: 100%;
  padding: 0.55rem 0.75rem;
  border: 1px solid rgba(180, 83, 9, 0.18);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.7);
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}
.subscribe-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.12);
  background: #fff;
}
.subscribe-input::placeholder { color: #b08968; }
.subscribe-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.subscribe-btn {
  width: 100%;
  padding: 0.55rem;
  background: linear-gradient(135deg, var(--primary-color), #f59e0b);
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  transition: all 0.25s ease;
}
.subscribe-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.35);
}
.subscribe-btn:active:not(:disabled) {
  transform: translateY(0);
}
.subscribe-btn.success {
  background: linear-gradient(135deg, #10b981, #059669);
}
.subscribe-btn:disabled {
  opacity: 0.85;
  cursor: not-allowed;
}

.spin-icon {
  width: 16px; height: 16px;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.subscribe-msg {
  margin: 0.4rem 0 0;
  font-size: 0.78rem;
  text-align: center;
  padding: 0.3rem 0.5rem;
  border-radius: 0.4rem;
}
.subscribe-msg.success {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
}
.subscribe-msg.error {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* 主内容区 */
.main-content {
  min-width: 0;
}

.content-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-light);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: var(--primary-color);
  background: rgba(217, 119, 6, 0.1);
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-weight: 500;
}

.filter-badge:hover {
  background: rgba(217, 119, 6, 0.18);
}

.clear-filter-btn {
  font-size: 0.8rem;
  color: #fff;
  background: var(--primary-color);
  border: none;
  cursor: pointer;
  padding: 0.375rem 0.875rem;
  border-radius: 0.5rem;
  transition: all var(--transition-fast);
  font-weight: 500;
}

.clear-filter-btn:hover {
  background: var(--secondary-color);
  transform: translateY(-1px);
}

.content-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.content-count {
  font-size: 0.875rem;
  color: var(--text-muted);
  background: rgba(217, 119, 6, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
}

/* 动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== 响应式适配 ===== */
@media (max-width: 992px) {
  .content-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
  }
  
  .sidebar-section {
    margin-bottom: 0;
  }

  .archive-months {
    padding-left: 1.2rem;
  }
}

@media (max-width: 768px) {
  #texts-page {
    padding: 90px 1rem 3rem;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .page-title {
    font-size: 1.875rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }

  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
    padding: 1rem;
  }
  
  .stat-icon {
    margin-bottom: 0.5rem;
  }

  .stat-value {
    font-size: 1.25rem;
  }
  
  .content-header {
    flex-direction: column;
    gap: 0.75rem;
    align-items: flex-start;
  }
  
  .header-left {
    flex-wrap: wrap;
  }
  
  .header-right {
    width: 100%;
    justify-content: space-between;
  }
  
  .sidebar {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>