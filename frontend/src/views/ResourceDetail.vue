<template>
  <div class="resource-detail">
    <!-- 页面背景 -->
    <div class="page-background"></div>

    <!-- 返回按钮 -->
    <div class="back-button" @click="goBack">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M19 12H5M12 19l-7-7 7-7"/>
      </svg>
      <span>返回</span>
    </div>

    <div class="detail-container">
      <!-- 资源头部信息 -->
      <div class="resource-header">
        <div class="resource-icon-wrapper">
          <div class="resource-icon" :class="resource.icon">
            <component :is="getIcon(resource.icon)" />
          </div>
          <div class="icon-glow"></div>
        </div>
        
        <div class="resource-info">
          <div class="resource-badge">{{ resource.category }}</div>
          <h1 class="resource-title">{{ resource.title }}</h1>
          <p class="resource-desc">{{ resource.description }}</p>
          
          <div class="resource-meta">
            <span class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
              {{ resource.fileSize }}
            </span>
            <span class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 8v4l3 3"/>
                <circle cx="12" cy="12" r="10"/>
              </svg>
              {{ resource.uploadTime }}
            </span>
            <span class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              {{ resource.uploader }}
            </span>
          </div>
        </div>
      </div>

      <!-- 操作按钮区 -->
      <div class="action-bar">
        <button class="btn btn-primary" @click="downloadResource">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span>立即下载</span>
        </button>
        
        <button class="btn btn-secondary" @click="previewResource">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
          <span>在线预览</span>
        </button>
        
        <button class="btn btn-outline" @click="copyLink">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
          <span>复制链接</span>
        </button>
      </div>

      <!-- 资源详情标签页 -->
      <div class="detail-content">
        <div class="tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['tab', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            {{ tab.name }}
          </button>
        </div>

        <div class="tab-content">
          <!-- 详情页 -->
          <div v-if="activeTab === 'detail'" class="tab-panel">
            <h3 class="panel-title">资源介绍</h3>
            <p class="panel-text">{{ resource.intro }}</p>
            
            <h3 class="panel-title">文件信息</h3>
            <div class="info-grid">
              <div class="info-card">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10 9 9 9 8 9"/>
                </svg>
                <div>
                  <span class="info-label">文件名</span>
                  <span class="info-value">{{ resource.filename }}</span>
                </div>
              </div>
              <div class="info-card">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                  <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                  <line x1="12" y1="22.08" x2="12" y2="12"/>
                </svg>
                <div>
                  <span class="info-label">文件类型</span>
                  <span class="info-value">{{ resource.fileType }}</span>
                </div>
              </div>
              <div class="info-card">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <polyline points="21 15 16 10 5 21"/>
                </svg>
                <div>
                  <span class="info-label">文件大小</span>
                  <span class="info-value">{{ resource.fileSize }}</span>
                </div>
              </div>
              <div class="info-card">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2z"/>
                </svg>
                <div>
                  <span class="info-label">更新时间</span>
                  <span class="info-value">{{ resource.updateTime }}</span>
                </div>
              </div>
            </div>

            <h3 class="panel-title">使用说明</h3>
            <ul class="usage-list">
              <li v-for="(step, index) in resource.usage" :key="index">
                <span class="step-number">{{ index + 1 }}</span>
                <span>{{ step }}</span>
              </li>
            </ul>
          </div>

          <!-- 相关资源 -->
          <div v-if="activeTab === 'related'" class="tab-panel">
            <div class="related-grid">
              <div 
                v-for="item in relatedResources" 
                :key="item.id"
                class="related-card"
                @click="goToResource(item.id)"
              >
                <div class="related-icon" :class="item.icon">
                  <component :is="getIcon(item.icon)" />
                </div>
                <div class="related-info">
                  <h4 class="related-title">{{ item.title }}</h4>
                  <p class="related-desc">{{ item.description }}</p>
                  <span class="related-size">{{ item.fileSize }}</span>
                </div>
                <svg class="arrow-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </div>
          </div>

          <!-- 评论页 -->
          <div v-if="activeTab === 'comments'" class="tab-panel">
            <div class="comment-section">
              <div class="comment-input-wrapper">
                <div class="comment-avatar">U</div>
                <textarea 
                  v-model="newComment"
                  placeholder="分享您的想法..."
                  class="comment-input"
                  @keyup.enter.ctrl="submitComment"
                ></textarea>
                <button class="submit-comment-btn" @click="submitComment">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                  </svg>
                </button>
              </div>

              <div class="comments-list">
                <div v-for="comment in comments" :key="comment.id" class="comment-item">
                  <div class="comment-avatar">{{ comment.avatar }}</div>
                  <div class="comment-content">
                    <div class="comment-header">
                      <span class="comment-author">{{ comment.author }}</span>
                      <span class="comment-time">{{ comment.time }}</span>
                    </div>
                    <p class="comment-text">{{ comment.content }}</p>
                    <div class="comment-actions">
                      <button class="action-btn">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                        </svg>
                        <span>{{ comment.likes }}</span>
                      </button>
                      <button class="action-btn">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M8 15a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm4-1a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3-1a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
                        </svg>
                        <span>回复</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast 提示 -->
    <transition name="toast">
      <div v-if="toast.show" class="toast">
        {{ toast.message }}
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Document, 
  Files, 
  Briefcase,
  Picture as ImageIcon
} from '@element-plus/icons-vue'

const router = useRouter()

const activeTab = ref('detail')
const newComment = ref('')

const toast = reactive({
  show: false,
  message: ''
})

const tabs = [
  { id: 'detail', name: '详情' },
  { id: 'related', name: '相关资源' },
  { id: 'comments', name: '评论' }
]

const resource = reactive({
  id: '1',
  title: '后端开发实习生简历模板',
  description: '适合后端开发实习生岗位的简历模板，包含项目经验、技能展示等模块',
  category: '简历模板',
  icon: 'FileText',
  filename: '后端开发实习生简历.pdf',
  fileType: 'PDF 文件',
  fileSize: '1.2 MB',
  uploadTime: '2024-06-15',
  updateTime: '2024-06-20',
  uploader: '管理员',
  intro: '本简历模板专为后端开发实习生设计，包含个人信息、技能展示、项目经验、教育背景等模块。模板采用简洁专业的设计风格，适合投递各类互联网公司的后端开发岗位。',
  usage: [
    '下载并使用 PDF 阅读器打开模板',
    '根据实际情况修改个人信息',
    '调整技能熟练度和项目经验描述',
    '导出为 PDF 格式用于投递'
  ]
})

const relatedResources = [
  { id: '2', title: '前端开发简历模板', description: '适合前端开发岗位的精美简历模板', fileSize: '856 KB', icon: 'FileText' },
  { id: '3', title: '全栈开发学习路线', description: '从入门到精通的全栈开发学习指南', fileSize: '2.1 MB', icon: 'FileCode' },
  { id: '4', title: '面试题精选合集', description: '包含各大厂面试题及答案解析', fileSize: '3.5 MB', icon: 'FileArchive' },
  { id: '5', title: '项目经验案例库', description: '优秀项目经验描述参考', fileSize: '1.8 MB', icon: 'FileText' }
]

const comments = [
  { id: '1', author: '开发者小王', avatar: 'W', time: '2小时前', content: '这个模板很实用，已经用上了！', likes: 12 },
  { id: '2', author: '应届生小李', avatar: 'L', time: '1天前', content: '感谢分享，对我帮助很大', likes: 8 },
  { id: '3', author: 'HR小张', avatar: 'Z', time: '3天前', content: '模板格式清晰，内容完整', likes: 15 }
]

const iconMap: Record<string, any> = {
  FileText: Document,
  FileImage: ImageIcon,
  FileCode: Briefcase,
  FileArchive: Files,
  FileMusic: Document,
  FileVideo: ImageIcon
}

const getIcon = (iconName: string) => {
  return iconMap[iconName] || Document
}

const goBack = () => {
  router.back()
}

const downloadResource = () => {
  showToast('正在下载...')
}

const previewResource = () => {
  showToast('预览功能开发中')
}

const copyLink = () => {
  navigator.clipboard.writeText(window.location.href)
  showToast('链接已复制')
}

const goToResource = (id: string) => {
  showToast(`正在打开资源 ${id}`)
}

const submitComment = () => {
  if (!newComment.value.trim()) return
  showToast('评论提交成功')
  newComment.value = ''
}

const showToast = (message: string) => {
  toast.message = message
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 2000)
}
</script>

<style scoped>
/* ===== 暖色系变量定义 ===== */
.resource-detail {
  --primary: #d97706;
  --primary-light: #f59e0b;
  --primary-dark: #b45309;
  --primary-glow: rgba(217, 119, 6, 0.3);
  
  --text-main: #451a03;
  --text-sub: #78350f;
  --text-muted: #92400e;
  
  --bg-page: #FFFBEB;
  --bg-card: rgba(255, 255, 255, 0.9);
  --bg-card-hover: rgba(255, 255, 255, 0.98);
  
  --border: rgba(180, 83, 9, 0.1);
  --border-hover: rgba(217, 119, 6, 0.3);
  
  --shadow-soft: 0 4px 20px rgba(139, 69, 19, 0.06);
  --shadow-card: 0 8px 32px rgba(139, 69, 19, 0.08);
  --shadow-hover: 0 16px 40px rgba(139, 69, 19, 0.15);
  
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.25rem;
  
  min-height: 100vh;
  padding: 100px 1.5rem 4rem;
  position: relative;
  z-index: 1;
}

/* 页面背景 */
.page-background {
  position: fixed;
  inset: 0;
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF9C3 50%, #FEFCE8 100%);
  z-index: -1;
  pointer-events: none;
}

.page-background::before {
  content: '';
  position: absolute;
  top: -20%;
  right: -20%;
  width: 60%;
  height: 60%;
  background: radial-gradient(circle, var(--primary-glow) 0%, transparent 70%);
  animation: floatGlow 15s ease-in-out infinite;
}

@keyframes floatGlow {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.6; }
  50% { transform: translate(30px, -30px) scale(1.1); opacity: 0.8; }
}

/* 返回按钮 */
.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 2rem;
}

.back-button:hover {
  color: var(--primary);
  border-color: var(--primary);
  background: rgba(217, 119, 6, 0.05);
}

/* 容器 */
.detail-container {
  max-width: 900px;
  margin: 0 auto;
}

/* 资源头部 */
.resource-header {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-card);
  margin-bottom: 1.5rem;
}

.resource-icon-wrapper {
  position: relative;
}

.resource-icon {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  box-shadow: 0 8px 24px rgba(217, 119, 6, 0.3);
  transition: transform 0.3s ease;
}

.resource-icon:hover {
  transform: scale(1.05);
}

.icon-glow {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: radial-gradient(circle, rgba(217, 119, 6, 0.2) 0%, transparent 70%);
  border-radius: 1.5rem;
  animation: pulseGlow 3s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}

.resource-info {
  flex: 1;
}

.resource-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: rgba(217, 119, 6, 0.1);
  color: var(--primary);
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 9999px;
  margin-bottom: 0.75rem;
}

.resource-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0 0 0.75rem;
}

.resource-desc {
  color: var(--text-sub);
  font-size: 1rem;
  line-height: 1.6;
  margin: 0 0 1rem;
}

.resource-meta {
  display: flex;
  gap: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  color: var(--text-muted);
}

/* 操作按钮区 */
.action-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  font-family: inherit;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(217, 119, 6, 0.4);
}

.btn-secondary {
  background: rgba(217, 119, 6, 0.1);
  color: var(--primary);
  border: 1px solid rgba(217, 119, 6, 0.2);
}

.btn-secondary:hover {
  background: rgba(217, 119, 6, 0.15);
  border-color: var(--primary);
}

.btn-outline {
  background: transparent;
  color: var(--text-sub);
  border: 1px solid var(--border);
}

.btn-outline:hover {
  color: var(--primary);
  border-color: var(--primary);
  background: rgba(217, 119, 6, 0.05);
}

/* 详情内容区 */
.detail-content {
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
}

.tab {
  padding: 1.25rem 2rem;
  background: transparent;
  border: none;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.tab:hover {
  color: var(--primary);
}

.tab.active {
  color: var(--primary);
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 2rem;
  right: 2rem;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--primary-light));
  border-radius: 9999px;
}

.tab-content {
  padding: 2rem;
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.panel-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
  margin: 0 0 1rem;
}

.panel-text {
  color: var(--text-sub);
  line-height: 1.7;
  margin: 0 0 2rem;
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(217, 119, 6, 0.03);
  border-radius: var(--radius-md);
  color: var(--text-muted);
}

.info-card div {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.75rem;
}

.info-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-main);
}

/* 使用说明 */
.usage-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.usage-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
}

.usage-list li:last-child {
  border-bottom: none;
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 50%;
  flex-shrink: 0;
}

/* 相关资源 */
.related-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.related-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(217, 119, 6, 0.03);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.related-card:hover {
  background: rgba(217, 119, 6, 0.08);
  border-color: var(--border);
  transform: translateX(4px);
}

.related-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: white;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
}

.related-info {
  flex: 1;
}

.related-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-main);
  margin: 0 0 0.25rem;
}

.related-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 0;
}

.related-size {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.arrow-icon {
  color: var(--text-muted);
  transition: all 0.2s ease;
}

.related-card:hover .arrow-icon {
  color: var(--primary);
  transform: translateX(4px);
}

/* 评论区 */
.comment-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment-input-wrapper {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(217, 119, 6, 0.03);
  border-radius: var(--radius-lg);
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  flex-shrink: 0;
}

.comment-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  resize: none;
  background: white;
  color: var(--text-main);
  transition: all 0.2s ease;
}

.comment-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.1);
}

.comment-input::placeholder {
  color: var(--text-muted);
}

.submit-comment-btn {
  padding: 0.75rem 1rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-comment-btn:hover {
  background: var(--primary-dark);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  display: flex;
  gap: 0.75rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 600;
  color: var(--text-main);
  font-size: 0.9rem;
}

.comment-time {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.comment-text {
  color: var(--text-sub);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 0.5rem;
}

.comment-actions {
  display: flex;
  gap: 1.5rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  color: var(--primary);
}

/* Toast */
.toast {
  position: fixed;
  bottom: 3rem;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.75rem 1.5rem;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  font-size: 0.875rem;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-hover);
  z-index: 9999;
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
}

/* ===== 响应式适配 ===== */
@media (max-width: 768px) {
  .resource-detail {
    padding: 80px 1rem 3rem;
  }
  
  .resource-header {
    flex-direction: column;
    text-align: center;
  }
  
  .resource-icon-wrapper {
    margin: 0 auto;
  }
  
  .resource-meta {
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
  }
  
  .action-bar {
    flex-wrap: wrap;
  }
  
  .btn {
    flex: 1;
    min-width: 120px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .tab {
    padding: 1rem;
    font-size: 0.875rem;
  }
  
  .tab-content {
    padding: 1.25rem;
  }
}
</style>