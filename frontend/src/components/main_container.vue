<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
// 1. 在 Script 中正确引入图标组件
import { Calendar, Reading, View, ChatDotRound, Picture } from '@element-plus/icons-vue'
import { get_texts } from '../api/api'
import type { PostItem, ApiResponse } from '../api/api'
import { formatDate, normalizeTags, filterMarkdown, truncateText } from '../utils/index'

const router = useRouter()

const rawResponse = ref<ApiResponse<PostItem[]> | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const parsePostArray = (arr: any[]): PostItem => ({
  id: arr[0] ?? 0,
  user_id: arr[1] ?? 0,
  title: arr[2] ?? '无标题',
  content: arr[4] ?? '',
  content_type: arr[5] ?? 'markdown',
  summary: arr[6] ?? '',
  cover_img: arr[7] ?? '',
  views: arr[8] ?? 0,
  tags: arr[9] ?? '',
  status: arr[10] ?? 1,
  visibility: arr[11] ?? 1,
  likes: arr[13] ?? 0,
  comments_count: arr[14] ?? 0,
  created_at: arr[16] ?? new Date().toISOString(),
  updated_at: arr[17] ?? new Date().toISOString()
})

const postList = computed<PostItem[]>(() => {
  if (!rawResponse.value?.data) return []
  const data = rawResponse.value.data
  if (!Array.isArray(data)) return []
  
  return data
    .map(item => Array.isArray(item) ? parsePostArray(item) : null)
    .filter((item): item is PostItem => item !== null)
    .slice(0, 12)
})

const fetchData = async () => {
  loading.value = true
  error.value = null
  try {
    rawResponse.value = await get_texts()
  } catch (err) {
    console.error('Fetch posts error:', err)
    error.value = err instanceof Error ? err.message : '数据获取失败'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

const handleCardClick = (id: number) => {
  router.push({
    name: 'PostDetail',
    params: { id: String(id) }
  })
}
</script>

<template>
  <div class="blog-list-container">
    <!-- 骨架屏 -->
    <div v-if="loading" class="skeleton-grid">
      <div v-for="i in 6" :key="i" class="glass-card-skeleton">
        <div class="skeleton-cover"></div>
        <div class="skeleton-content">
          <div class="skeleton-header">
            <div class="skeleton-tag"></div>
            <div class="skeleton-date"></div>
          </div>
          <div class="skeleton-title"></div>
          <div class="skeleton-text line-1"></div>
          <div class="skeleton-text line-2"></div>
          <div class="skeleton-footer"></div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <el-result v-else-if="error" icon="error" title="加载失败" :sub-title="error">
      <template #extra>
        <el-button type="primary" @click="fetchData" round>重新加载</el-button>
      </template>
    </el-result>

    <!-- 空状态 -->
    <el-empty v-else-if="postList.length === 0" description="暂无发布文章" />

    <!-- 文章列表 -->
    <TransitionGroup v-else name="list" tag="div" class="post-grid">
      <article
        v-for="(item) in postList"
        :key="item.id"
        class="post-card"
        @click="handleCardClick(item.id)"
      >
        <div class="card-glow"></div>
        
        <div v-if="item.cover_img" class="post-cover-wrapper">
          <el-image 
            :src="item.cover_img" 
            fit="cover" 
            class="post-cover" 
            lazy
          >
            <template #error>
              <div class="image-error-slot">
                <!-- 这里使用在 script 中引入的 Picture 图标 -->
                <el-icon><Picture /></el-icon>
              </div>
            </template>
          </el-image>
          <div class="cover-overlay"></div>
        </div>

        <div class="card-body">
          <div class="card-header">
            <div class="tag-list" v-if="item.tags">
              <span 
                v-for="tag in normalizeTags(item.tags).slice(0, 2)" 
                :key="tag" 
                class="tag-badge"
              >
                {{ tag }}
              </span>
            </div>
            <div class="post-date">
              <el-icon><Calendar /></el-icon>
              <span>{{ formatDate(item.created_at, 'MM-DD') }}</span>
            </div>
          </div>

          <h3 class="post-title">{{ item.title }}</h3>

          <p class="post-excerpt">
            {{ item.summary || truncateText(filterMarkdown(item.content), 100) }}
          </p>

          <div class="post-footer">
            <div class="post-stats">
              <div class="stat-item">
                <el-icon><View /></el-icon>
                <span>{{ item.views }}</span>
              </div>
              <div class="stat-item">
                <el-icon><ChatDotRound /></el-icon>
                <span>{{ item.comments_count }}</span>
              </div>
            </div>
            <div class="read-more">
              <span>阅读全文</span>
              <el-icon class="arrow-icon"><Reading /></el-icon>
            </div>
          </div>
        </div>
      </article>
    </TransitionGroup>
  </div>
</template>

<style scoped>
/* 
   注意：千万不要在这里写 @import '@element-plus/icons-vue' 
   CSS 只能导入 .css, .scss, .less 等样式文件 
*/

.blog-list-container {
  width: 100%;
}

.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.post-card {
  position: relative;
  background: rgba(30, 41, 59, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.post-card:hover {
  transform: translateY(-6px);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

.card-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    800px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
    rgba(99, 102, 241, 0.06),
    transparent 40%
  );
  z-index: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.post-card:hover .card-glow {
  opacity: 1;
}

.post-cover-wrapper {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
  z-index: 1;
}

.post-cover {
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease;
}

.post-card:hover .post-cover {
  transform: scale(1.05);
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(15, 23, 42, 0.6) 100%);
  pointer-events: none;
}

.image-error-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #1e293b;
  color: #475569;
  font-size: 2rem;
}

.card-body {
  position: relative;
  z-index: 1;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 0.75rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.25rem;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  flex: 1;
}

.tag-badge {
  font-size: 0.75rem;
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.post-date {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  color: #94a3b8;
  white-space: nowrap;
}

.post-title {
  font-size: 1.125rem;
  color: #f1f5f9;
  margin: 0;
  font-weight: 600;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.post-card:hover .post-title {
  color: #818cf8;
}

.post-excerpt {
  color: #cbd5e1;
  line-height: 1.6;
  font-size: 0.875rem;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  margin-top: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.post-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  color: #64748b;
}

.read-more {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #818cf8;
  transition: gap 0.2s ease;
}

.post-card:hover .read-more {
  gap: 8px;
}

/* 骨架屏 */
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.glass-card-skeleton {
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  overflow: hidden;
  height: 320px;
}

.skeleton-cover {
  height: 180px;
  background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
}

.skeleton-tag, .skeleton-date, .skeleton-title, .skeleton-text, .skeleton-footer {
  background: #334155;
  border-radius: 4px;
  animation: shimmer 1.5s infinite;
}

.skeleton-tag { width: 60px; height: 20px; }
.skeleton-date { width: 50px; height: 20px; }
.skeleton-title { height: 24px; width: 80%; }
.skeleton-text { height: 16px; width: 100%; }
.skeleton-footer { margin-top: auto; height: 20px; width: 40%; }

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

@media (max-width: 768px) {
  .post-grid, .skeleton-grid {
    grid-template-columns: 1fr;
  }
}
</style>