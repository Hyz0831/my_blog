<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElCard, ElTag, ElPagination, ElEmpty } from 'element-plus'
import { useRouter } from 'vue-router'
import { get_texts, get_posts_by_tags } from '../api/api.ts'
import type { PostItem, ApiResponse } from '../api/api.ts'
import { formatDate, normalizeTags, truncateText, filterMarkdown } from '../utils/index'

interface FilterParams {
  category?: string
  tags?: string[]
}

const router = useRouter()

const articles = ref<PostItem[]>([])
const currentPage = ref(1)
const pageSize = ref(6)
const totalArticles = ref(0)
const loading = ref(false)
const currentFilter = ref<FilterParams>({})
const isEmptyResult = ref(false)

const truncateContent = (content: string): string => {
  if (!content) return '暂无简介'
  const plainText = filterMarkdown(content)
  const truncated = truncateText(plainText, 120)
  return truncated || '暂无简介'
}

const goToArticle = (id: number | string) => {
  router.push({ name: 'PostDetail', params: { id: String(id) } })
}

const loadArticles = async () => {
  loading.value = true
  isEmptyResult.value = false
  try {
      let response: ApiResponse<PostItem[]>
      
      const hasCategory = currentFilter.value.category && currentFilter.value.category !== 'all'
      const hasTags = currentFilter.value.tags && currentFilter.value.tags.length > 0
      
      if (hasTags || hasCategory) {
        response = await get_posts_by_tags(
          currentFilter.value.tags || [],
          currentFilter.value.category,
          currentPage.value,
          pageSize.value
        )
      } else {
        response = await get_texts(currentPage.value, pageSize.value)
      }
    
    articles.value = response.data || []
    totalArticles.value = response.total || 0
    if (articles.value.length === 0 && currentPage.value === 1) {
      isEmptyResult.value = true
    }
  } catch (error: any) {
    console.error('文章加载失败:', error)
    articles.value = []
    totalArticles.value = 0
    isEmptyResult.value = true
  } finally {
    loading.value = false
  }
}

const setFilter = (filter: FilterParams) => {
  currentFilter.value = { ...filter }
  currentPage.value = 1
  loadArticles()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadArticles()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

defineExpose({ setFilter })

onMounted(() => {
  loadArticles()
})
</script>

<template>
  <div id="blog-list-page">
    <div
        class="articles-container"
        v-loading="loading"
        element-loading-background="rgba(15, 23, 42, 0.8)"
    >
      <el-card
          v-for="(article, index) in articles"
          :key="article.id"
          class="article-card"
          @click="goToArticle(article.id)"
          :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="card-header">
          <div class="article-meta">
            <span class="date">{{ formatDate(article.created_at) }}</span>
          </div>
          <h2 class="article-title">{{ article.title }}</h2>
          <div class="tags-container">
            <el-tag
                v-for="tag in normalizeTags(article.tags)"
                :key="tag"
                size="small"
                class="article-tag"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <p class="article-excerpt">
          {{ article.summary ? filterMarkdown(article.summary) : truncateContent(article.content) }}
        </p>

        <div class="card-footer">
          <div class="stats-row">
            <span class="stat-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              {{ article.views || 0 }}
            </span>
            <span class="stat-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              {{ article.likes || 0 }}
            </span>
          </div>
          <span class="read-more">
            <span>阅读全文</span>
            <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 5l7 7-7 7"/>
            </svg>
          </span>
        </div>
      </el-card>

      <el-empty v-if="articles.length === 0 && !loading" :description="isEmptyResult ? '该筛选条件下暂无文章' : '暂无发布文章'">
        <template #image>
          <div class="empty-icon">📭</div>
        </template>
        <template #description>
          <p class="empty-text">{{ isEmptyResult ? '该筛选条件下暂无文章' : '暂无发布文章' }}</p>
          <button v-if="isEmptyResult" class="empty-action" @click="$emit('clear-filter')">
            清除筛选
          </button>
        </template>
      </el-empty>
    </div>

    <div class="pagination-container">
      <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="totalArticles"
          layout="prev, pager, next"
          @current-change="handlePageChange"
          background
      />
    </div>
  </div>
</template>

<style scoped>
/* ===== 暖色系变量定义 ===== */
#blog-list-page {
  --primary-color: #d97706;      /* Amber-600 */
  --secondary-color: #b45309;    /* Amber-700 */
  --accent-color: #f59e0b;       /* Amber-500 */
  
  --text-primary: #451a03;       /* Deep Brown */
  --text-secondary: #78350f;     /* Medium Brown */
  --text-muted: #92400e;         /* Light Brown */
  
  --bg-card: rgba(254, 243, 199, 0.6);  /* Amber-100 with opacity */
  --border-light: rgba(180, 83, 9, 0.15);
  --border-hover: rgba(217, 119, 6, 0.4);
  
  --shadow-md: 0 4px 20px rgba(139, 69, 19, 0.08);
  --shadow-lg: 0 12px 30px rgba(139, 69, 19, 0.12);
  
  --transition-fast: 0.2s ease;
  --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  --font-xs: 0.75rem;
  --font-sm: 0.875rem;
  --font-lg: 1.125rem;
  --font-xl: 1.5rem;
  
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  
  min-height: 100%;
}

/* 文章列表容器 */
.articles-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-xl);
}

/* 文章卡片 */
.article-card {
  background: var(--bg-card) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-light) !important;
  border-radius: var(--radius-2xl) !important;
  cursor: pointer;
  transition: all var(--transition-normal);
  overflow: hidden;
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
  box-shadow: var(--shadow-md);
}

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

.article-card:hover {
  transform: translateY(-5px);
  border-color: var(--border-hover) !important;
  box-shadow: var(--shadow-lg);
  background: rgba(254, 243, 199, 0.8) !important;
}

/* 卡片头部 */
.card-header {
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
}

.date {
  font-size: var(--font-xs);
  color: var(--text-muted);
  font-weight: 500;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.date::before {
  content: '';
  width: 4px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 50%;
}

/* 文章标题 */
.article-title {
  font-size: clamp(var(--font-lg), 3vw, var(--font-xl));
  font-weight: 700;
  color: var(--text-primary);
  margin: var(--spacing-sm) 0;
  line-height: 1.4;
  transition: color var(--transition-fast);
}

.article-card:hover .article-title {
  color: var(--primary-color);
}

/* 标签容器 */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
}

.article-tag {
  background: rgba(217, 119, 6, 0.12) !important;
  border-color: rgba(217, 119, 6, 0.25) !important;
  color: var(--secondary-color) !important;
  font-size: var(--font-xs);
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 9999px;
  transition: all var(--transition-fast);
}

.article-tag:hover {
  background: rgba(217, 119, 6, 0.18) !important;
  border-color: var(--primary-color) !important;
  transform: translateY(-1px);
}

/* 文章摘要 */
.article-excerpt {
  color: var(--text-secondary);
  font-size: var(--font-sm);
  line-height: 1.8;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: rgba(255, 255, 255, 0.5);
  border-radius: var(--radius-lg);
}

/* 卡片底部 */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-light);
}

.stats-row {
  display: flex;
  gap: var(--spacing-lg);
  font-size: var(--font-xs);
  color: var(--text-muted);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 阅读全文按钮 */
.read-more {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--primary-color);
  font-size: var(--font-sm);
  font-weight: 500;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-lg);
  background: rgba(217, 119, 6, 0.08);
  border: 1px solid transparent;
  transition: all var(--transition-fast);
}

.read-more:hover {
  background: rgba(217, 119, 6, 0.15);
  border-color: rgba(217, 119, 6, 0.3);
  transform: translateX(4px);
}

.arrow-icon {
  width: 16px;
  height: 16px;
  transition: transform var(--transition-fast);
}

.read-more:hover .arrow-icon {
  transform: translateX(4px);
}

/* 分页容器 */
.pagination-container {
  margin-top: var(--spacing-xl);
  display: flex;
  justify-content: center;
  padding-bottom: var(--spacing-xl);
}

/* Element Plus 分页样式覆盖 */
:deep(.el-pagination) {
  --el-pagination-button-bg-color: transparent;
  --el-pagination-button-text-color: var(--text-secondary);
  --el-pagination-button-hover-bg-color: rgba(217, 119, 6, 0.1);
  --el-pagination-button-hover-text-color: var(--primary-color);
  --el-pagination-button-active-bg-color: rgba(217, 119, 6, 0.15);
  --el-pagination-button-active-text-color: var(--primary-color);
}

/* 空状态自定义 */
.empty-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.empty-text {
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.empty-action {
  padding: 0.5rem 1.25rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all var(--transition-fast);
}

.empty-action:hover {
  background: var(--secondary-color);
  transform: translateY(-1px);
}

:deep(.el-pagination .btn-next),
:deep(.el-pagination .btn-prev) {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

:deep(.el-pagination .number) {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  margin: 0 2px;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .articles-container {
    gap: var(--spacing-lg);
  }
  
  .article-title {
    font-size: var(--font-lg);
  }

  .article-excerpt {
    font-size: var(--font-xs);
    line-height: 1.6;
  }
  
  .card-footer {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: flex-start;
  }
  
  .stats-row {
    order: 2;
  }
  
  .read-more {
    order: 1;
  }
}

@media (max-width: 480px) {
  .article-card {
    padding: var(--spacing-md) !important;
  }
  
  .card-header {
    padding-bottom: var(--spacing-sm);
  }
  
  .article-excerpt {
    padding: var(--spacing-sm);
  }
}
</style>
