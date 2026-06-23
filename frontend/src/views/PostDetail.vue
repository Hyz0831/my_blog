<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { get_text_detail } from '../api/api.ts'
import { throttle } from '../utils/index'
import { ArrowLeft, Calendar, View, Star, Share, PriceTag, Reading, Picture as ImageIcon } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { PostItem, ApiResponse } from '../api/api.ts'

const route = useRoute()
const router = useRouter()

const post = ref<PostItem | null>(null)
const loading = ref(true)
const progress = ref(0)
const imageLoaded = ref(false)
const imageError = ref(false)

const cleanCoverImg = (img: string | null): string | null => {
  if (!img) return null
  return img.replace(/^[`'"]+|[`'"]+$/g, '').trim()
}

const parsePostArray = (arr: unknown[]): PostItem => {
  if (!Array.isArray(arr) || arr.length < 18) {
    throw new Error('数组格式不正确或长度不足')
  }
  return {
    id: Number(arr[0]) || 0,
    user_id: Number(arr[1]) || 0,
    title: String(arr[2] || ''),
    content: String(arr[4] || ''),
    content_type: String(arr[5] || ''),
    summary: arr[6] ? String(arr[6]) : '',
    cover_img: cleanCoverImg(arr[7] ? String(arr[7]) : null) || '',
    views: Number(arr[8]) || 0,
    tags: (arr[9] as string | string[]) || [],
    status: Number(arr[10]) || 0,
    visibility: Number(arr[11]) || 0,
    likes: Number(arr[13]) || 0,
    comments_count: Number(arr[14]) || 0,
    created_at: String(arr[16] || ''),
    updated_at: String(arr[17] || '')
  }
}

const tags = computed<string[]>(() => {
  const rawTags = post.value?.tags
  if (!rawTags) return []
  if (Array.isArray(rawTags)) return rawTags
  if (typeof rawTags === 'string') {
    if (rawTags.startsWith('[')) {
      try { return JSON.parse(rawTags) } catch (e) { return [] }
    }
    return rawTags.split(',').map((t: string) => t.trim())
  }
  return []
})

const hasContent = computed(() => {
  const c = post.value?.content
  return Boolean(c && c.trim().length > 0)
})

const readingTime = computed(() => {
  const contentLength = post.value?.content?.length || 0
  return Math.ceil(contentLength / 400)
})

const formatDate = (dateStr: string): string => {
  if (!dateStr) return '未知时间'
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return dateStr
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${minutes}`
  } catch {
    return dateStr
  }
}

const handleImageLoad = () => {
  imageLoaded.value = true
}

const handleImageError = () => {
  imageLoaded.value = true
  imageError.value = true
}



const fetchData = async () => {
  loading.value = true
  try {
    const id = route.params.id
    if (!id || (typeof id !== 'string' && typeof id !== 'number')) {
      ElMessage.error('无效的文章 ID')
      return
    }

    const numericId = typeof id === 'string' ? parseInt(id) : id
    if (isNaN(numericId)) {
      ElMessage.error('无效的文章 ID')
      return
    }

    const res: ApiResponse<PostItem> = await get_text_detail(numericId)
    const dataArray = res.data

    if (Array.isArray(dataArray)) {
      post.value = parsePostArray(dataArray)
    } else if (dataArray && typeof dataArray === 'object') {
      post.value = dataArray as PostItem
    } else {
      ElMessage.error('数据格式错误')
      return
    }
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : '未知错误'
    ElMessage.error(`获取文章失败: ${errorMessage}`)
  } finally {
    loading.value = false
  }
}

const handleScroll = () => {
  const scrollH = document.documentElement.scrollHeight - document.documentElement.clientHeight
  const scrollTop = document.documentElement.scrollTop || document.body.scrollTop
  progress.value = scrollH > 0 ? (scrollTop / scrollH) * 100 : 0
}

const throttledHandleScroll = throttle(handleScroll, 150)

onMounted(() => {
  window.addEventListener('scroll', throttledHandleScroll)
  fetchData()
})

onUnmounted(() => {
  window.removeEventListener('scroll', throttledHandleScroll)
})
</script>

<template>
  <div class="post-detail-layout">
    <!-- 顶部阅读进度条 -->
    <div class="reading-progress" :style="{ width: progress + '%' }"></div>

    <div class="post-container">
      <!-- 主内容区 -->
      <main class="post-main-content">
        <el-skeleton :loading="loading" animated :rows="10" class="skeleton-wrapper">
          <template #default>
            <article v-if="post" class="post-article">
              <!-- 封面图 -->
              <div v-if="post.cover_img" class="post-banner">
                <div v-if="!imageLoaded" class="banner-loading">
                  <el-skeleton animated class="banner-skeleton" />
                </div>
                <el-image 
                  v-show="imageLoaded && !imageError"
                  :src="post.cover_img" 
                  fit="cover" 
                  lazy
                  @load="handleImageLoad"
                  @error="handleImageError"
                />
                <div v-if="imageError" class="banner-error">
                  <ImageIcon class="error-icon" />
                  <span class="error-text">图片加载失败</span>
                </div>
                <div class="banner-gradient"></div>
              </div>

              <div class="article-inner">
                <!-- 头部信息 -->
                <header class="article-header">
                  <button class="btn-back" @click="router.back()">
                    <ArrowLeft class="back-icon" /> <span>返回列表</span>
                  </button>
                  <h1 class="article-title">{{ post.title }}</h1>

                  <div class="article-meta">
                    <div class="meta-left">
                      <span class="meta-item"><Calendar class="meta-icon" /> {{ formatDate(post.created_at) }}</span>
                      <span class="meta-item"><View class="meta-icon" /> {{ post.views }}</span>
                      <span class="meta-item"><Reading class="meta-icon" /> {{ readingTime }} min</span>
                    </div>
                    <div class="tags-row">
                      <span v-for="tag in tags" :key="tag" class="tag-chip"><PriceTag class="tag-icon" /> {{ tag }}</span>
                    </div>
                  </div>
                </header>

                <!-- 正文内容（限制最大宽度保障阅读体验） -->
                <div class="markdown-container">
                  <div v-if="hasContent" class="markdown-body">
                    <v-md-preview
                      :text="post.content || ''"
                      class="markdown-body"
                    />
                  </div>
                  <div v-else class="empty-content-placeholder">
                    <Reading class="placeholder-icon" />
                    <p>该文章暂无正文内容</p>
                  </div>
                </div>

                <!-- 底部操作与更新 -->
                <footer class="article-footer">
                  <div class="footer-actions">
                    <button class="btn-action"><Star /> {{ post.likes }}</button>
                    <button class="btn-action"><Share /> 分享</button>
                  </div>
                  <p class="last-updated">最后更新于 {{ formatDate(post.updated_at) }}</p>
                </footer>
              </div>
            </article>
            <el-empty v-else description="文章加载失败" :image-size="60" />
          </template>
        </el-skeleton>

        <!-- 评论区 -->
        <section class="comments-section">
          <h3 class="section-heading">💬 评论交流</h3>
          <div class="comments-placeholder">
            <el-empty description="评论功能开发中..." :image-size="60" />
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* ===== 布局与间距系统 ===== */
.post-detail-layout {
  --nav-height: 70px;
  --content-max-w: 760px; /* 最佳阅读宽度 (60-75字符) */

  --gap-xl: 2rem;
  --gap-lg: 1.5rem;
  --gap-md: 1rem;
  --gap-sm: 0.5rem;

  min-height: 100vh;
  padding-top: var(--nav-height);
  background: linear-gradient(180deg, #FFFBEB 0%, #FEF9E7 100%);
  position: relative;
}

/* 进度条 */
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #d97706, #f59e0b);
  z-index: 2000;
  transition: width 0.1s linear;
  box-shadow: 0 0 6px rgba(217, 119, 6, 0.4);
}

/* 主布局 */
.post-container {
  max-width: var(--content-max-w);
  margin: 0 auto;
  padding: 1.5rem;
}

.post-main-content { min-width: 0; }

/* 骨架屏 */
.skeleton-wrapper {
  background: rgba(254, 243, 199, 0.6);
  border: 1px solid rgba(180, 83, 9, 0.12);
  border-radius: 1rem;
  padding: var(--gap-xl);
}

/* 文章卡片 */
.post-article {
  background: rgba(254, 243, 199, 0.65);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(180, 83, 9, 0.12);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.06);
}

/* 封面图 */
.post-banner {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 6;
  max-height: 380px;
}
.post-banner .el-image { width: 100%; height: 100%; object-fit: cover; }
.banner-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 60%, rgba(254, 243, 199, 0.95) 100%);
}

/* 封面图加载状态 */
.banner-loading {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(254, 243, 199, 0.8);
}
.banner-skeleton {
  width: 100%;
  height: 100%;
}

/* 封面图错误状态 */
.banner-error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(254, 243, 199, 0.9);
  gap: 0.5rem;
}
.error-icon {
  width: 48px;
  height: 48px;
  color: #d97706;
  opacity: 0.6;
}
.error-text {
  color: #a38060;
  font-size: 0.875rem;
}

/* 文章内边距容器 */
.article-inner { padding: 0 var(--gap-xl) var(--gap-xl); }

/* 头部 */
.article-header { margin-bottom: var(--gap-lg); }
.btn-back {
  display: inline-flex;
  align-items: center;
  gap: var(--gap-sm);
  padding: 0.5rem 0.75rem;
  background: transparent;
  border: 1px solid rgba(180, 83, 9, 0.15);
  border-radius: 0.5rem;
  color: #92400e;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: var(--gap-md);
}
.btn-back:hover { 
  background: rgba(217, 119, 6, 0.1); 
  border-color: #d97706; 
  transform: translateX(-2px);
}
.back-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}
.btn-back:hover .back-icon {
  transform: translateX(-3px);
}

.article-title {
  font-size: clamp(1.75rem, 4vw, 2.25rem);
  font-weight: 700;
  color: #451a03;
  line-height: 1.3;
  margin: 0 0 var(--gap-md);
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: var(--gap-md);
  padding-bottom: var(--gap-md);
  border-bottom: 1px solid rgba(180, 83, 9, 0.12);
}
.meta-left { display: flex; gap: var(--gap-lg); color: #78350f; font-size: 0.875rem; }
.meta-item { display: flex; align-items: center; gap: 0.35rem; }
.meta-icon {
  width: 14px;
  height: 14px;
  color: #d97706;
}

.tags-row { display: flex; flex-wrap: wrap; gap: var(--gap-sm); }
.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.3rem 0.6rem;
  background: rgba(217, 119, 6, 0.12);
  border: 1px solid rgba(217, 119, 6, 0.25);
  border-radius: 999px;
  color: #b45309;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.2s ease;
}
.tag-chip:hover {
  background: rgba(217, 119, 6, 0.18);
  border-color: #d97706;
  transform: translateY(-1px);
}
.tag-icon {
  width: 12px;
  height: 12px;
}

/* Markdown 阅读区（核心优化：限制宽度） */
.markdown-container {
  max-width: var(--content-max-w);
  margin: 0 auto;
  padding-top: var(--gap-lg);
}
.markdown-body {
  background: transparent !important;
  color: #78350f;
  font-size: 1rem;
  line-height: 1.8;
}

/* Markdown 元素覆盖 */
:deep(.markdown-body h1), :deep(.markdown-body h2), :deep(.markdown-body h3), :deep(.markdown-body h4) {
  color: #451a03;
  font-weight: 600;
  margin: 2.5rem 0 1rem;
  scroll-margin-top: calc(var(--nav-height) + 20px);
}
:deep(.markdown-body h1) { font-size: 1.875rem; border-bottom: 1px solid rgba(180, 83, 9, 0.12); padding-bottom: 0.5rem; }
:deep(.markdown-body h2) { font-size: 1.5rem; }
:deep(.markdown-body h3) { font-size: 1.25rem; }
:deep(.markdown-body h4) { font-size: 1.125rem; }

:deep(.markdown-body p) { margin-bottom: 1.25rem; }
:deep(.markdown-body a) { color: #d97706; text-decoration: underline; text-underline-offset: 2px; }
:deep(.markdown-body a:hover) { color: #b45309; }
:deep(.markdown-body code) { background: rgba(217, 119, 6, 0.15); color: #b45309; padding: 0.2em 0.4em; border-radius: 0.3rem; font-family: ui-monospace, monospace; }
:deep(.markdown-body pre) { background: rgba(254, 243, 199, 0.5); border: 1px solid rgba(180, 83, 9, 0.12); border-radius: 0.75rem; padding: 1.25rem; overflow-x: auto; margin: 1.5rem 0; }
:deep(.markdown-body blockquote) { border-left: 4px solid #d97706; background: rgba(217, 119, 6, 0.06); padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 0.5rem 0.5rem 0; color: #92400e; font-style: italic; }
:deep(.markdown-body table) { width: 100%; border-collapse: collapse; margin: 1.5rem 0; border-radius: 0.5rem; overflow: hidden; border: 1px solid rgba(180, 83, 9, 0.12); }
:deep(.markdown-body th), :deep(.markdown-body td) { border: 1px solid rgba(180, 83, 9, 0.12); padding: 0.75rem; text-align: left; }
:deep(.markdown-body th) { background: rgba(217, 119, 6, 0.1); color: #451a03; font-weight: 600; }
:deep(.markdown-body img) { max-width: 100%; border-radius: 0.75rem; margin: 1.5rem 0; box-shadow: 0 4px 12px rgba(139, 69, 19, 0.08); }

/* 空内容占位 */
.empty-content-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 3rem 2rem;
  color: #92400e;
  font-size: 0.95rem;
}
.placeholder-icon {
  width: 48px;
  height: 48px;
  opacity: 0.4;
}

/* 底部 */
.article-footer {
  max-width: var(--content-max-w);
  margin: var(--gap-xl) auto 0;
  padding-top: var(--gap-lg);
  border-top: 1px solid rgba(180, 83, 9, 0.12);
  text-align: center;
}
.footer-actions { display: flex; justify-content: center; gap: var(--gap-md); margin-bottom: var(--gap-md); }
.btn-action {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.5rem 1rem; background: transparent; border: 1px solid rgba(180, 83, 9, 0.15);
  border-radius: 0.5rem; color: #78350f; cursor: pointer; transition: all 0.2s;
}
.btn-action:hover { background: rgba(217, 119, 6, 0.1); border-color: #d97706; transform: translateY(-2px); }
.last-updated { color: #a38060; font-size: 0.875rem; margin: 0; }

/* 评论区 */
.comments-section {
  margin-top: var(--gap-xl);
  background: rgba(254, 243, 199, 0.6);
  border: 1px solid rgba(180, 83, 9, 0.12);
  border-radius: 1rem;
  padding: var(--gap-xl);
}
.section-heading { font-size: 1.25rem; font-weight: 600; color: #451a03; margin: 0 0 var(--gap-lg); }
.comments-placeholder { padding: var(--gap-lg) 0; }

/* ===== 响应式布局 ===== */
@media (max-width: 768px) {
  .post-detail-layout { padding-top: 60px; }
  .post-container { padding: 1rem; }
  .article-inner { padding: 0 1.25rem 1.5rem; }
  .article-footer { padding: 0 1.25rem 1.5rem; }
  .post-banner { aspect-ratio: 16 / 9; max-height: 260px; }
  .article-meta { flex-direction: column; align-items: flex-start; gap: var(--gap-sm); }
  .tags-row { order: -1; }
}
</style>