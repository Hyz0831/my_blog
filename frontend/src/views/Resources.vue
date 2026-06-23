<template>
  <div class="resume-gallery">
    <!-- 页面背景 -->
    <div class="page-background"></div>

    <header class="gallery-header">
      <div class="header-icon">🔐</div>
      <h1 class="gallery-title">资源仓库</h1>
      <p class="gallery-subtitle">输入正确密码后可以获取专属资源</p>
    </header>

    <div class="resume-list">
      <div class="card-grid">
        <div
          v-for="item in resumeList"
          :key="item.id"
          class="resume-card"
          @click="handleCardClick(item)"
        >
          <div class="card-header">
            <div class="avatar">{{ getInitials(item.name) }}</div>
            <div class="header-info">
              <h3 class="name">{{ item.name }}</h3>
              <p class="role">{{ item.role }}</p>
            </div>
          </div>

          <div class="card-body">
            <div class="info-row">
              <el-icon class="info-icon"><User /></el-icon>
              <span>{{ item.experience }}</span>
            </div>
            <div class="info-row">
              <el-icon class="info-icon"><OfficeBuilding /></el-icon>
              <span>{{ item.company }}</span>
            </div>
            <div class="info-row">
              <el-icon class="info-icon"><Location /></el-icon>
              <span>{{ item.location }}</span>
            </div>

            <div class="skills">
              <el-tag
                v-for="skill in item.skills.slice(0, 3)"
                :key="skill"
                size="small"
                type="warning"
                effect="plain"
              >
                {{ skill }}
              </el-tag>
              <el-tag
                v-if="item.skills.length > 3"
                size="small"
                type="warning"
                effect="plain"
              >
                +{{ item.skills.length - 3 }}
              </el-tag>
            </div>
          </div>

          <div class="card-footer">
            <div class="lock-status">
              <el-icon><Lock /></el-icon>
              <span>需授权查看</span>
            </div>
            <el-button type="warning" size="small" plain>
              获取
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 密码验证对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="身份验证"
      width="420px"
      :close-on-click-modal="true"
      @closed="handleDialogClosed"
      class="warm-dialog"
    >
      <div class="dialog-content">
        <div class="dialog-avatar">{{ getInitials(currentItem?.name || '') }}</div>
        <p class="dialog-title">
          正在访问 <strong>{{ currentItem?.name }}</strong> 的资源
        </p>
        
        <el-form @submit.prevent="verifyPassword">
          <el-form-item>
            <el-input
              ref="passwordInputRef"
              v-model="password"
              type="password"
              placeholder="请输入访问密码"
              show-password
              size="large"
              @keyup.enter="verifyPassword"
              class="warm-input"
            />
          </el-form-item>
        </el-form>

        <transition name="fade">
          <p v-if="errorMessage" class="error-msg">
            <el-icon><Warning /></el-icon>
            {{ errorMessage }}
          </p>
        </transition>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" size="large">取消</el-button>
          <el-button
            type="warning"
            size="large"
            @click="verifyPassword"
            :loading="isVerifying"
          >
            确认访问
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { User, OfficeBuilding, Location, Lock, Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { get_resources, verify_resource_password } from '@/api/api'
import type { ResourceItem } from '@/api/api'

const router = useRouter()

const resumeList = ref<ResourceItem[]>([])
const loadingResources = ref(false)

const loadResources = async () => {
  loadingResources.value = true
  try {
    const result = await get_resources()
    resumeList.value = result.data || []
  } catch (error) {
    console.error('加载资源失败:', error)
    resumeList.value = []
  } finally {
    loadingResources.value = false
  }
}

onMounted(() => {
  loadResources()
})

const dialogVisible = ref(false)
const currentItem = ref<ResourceItem | null>(null)
const password = ref('')
const errorMessage = ref('')
const isVerifying = ref(false)
const passwordInputRef = ref<HTMLInputElement | null>(null)

const getInitials = (name: string): string => {
  return name ? name.charAt(0).toUpperCase() : '?'
}

const handleCardClick = (item: ResourceItem) => {
  currentItem.value = item
  password.value = ''
  errorMessage.value = ''
  isVerifying.value = false
  dialogVisible.value = true
  
  nextTick(() => {
    passwordInputRef.value?.focus()
  })
}

const handleDialogClosed = () => {
  currentItem.value = null
  password.value = ''
  errorMessage.value = ''
}

const verifyPassword = async () => {
  if (!password.value) {
    errorMessage.value = '密码不能为空'
    return
  }

  if (!currentItem.value?.id) {
    errorMessage.value = '资源信息无效'
    return
  }

  isVerifying.value = true
  errorMessage.value = ''

  try {
    const result = await verify_resource_password({
      resource_id: currentItem.value.id,
      password: password.value
    })

    if (result.code === 200) {
      ElMessage.success('验证成功，正在跳转...')
      dialogVisible.value = false
      
      if (result.data?.file_path) {
        window.open(result.data.file_path, '_blank')
      } else {
        router.push('/resources/detail')
      }
    } else {
      errorMessage.value = result.msg || '密码错误，请重新输入'
      password.value = ''
    }
  } catch (error: any) {
    errorMessage.value = error.message || '验证失败，请稍后重试'
    password.value = ''
  } finally {
    isVerifying.value = false
  }
}
</script>

<style scoped>
/* ===== 暖色系变量定义 ===== */
.resume-gallery {
  --primary: #d97706;
  --primary-light: #f59e0b;
  --primary-dark: #b45309;
  --primary-glow: rgba(217, 119, 6, 0.3);
  
  --text-main: #451a03;
  --text-sub: #78350f;
  --text-muted: #92400e;
  
  --bg-page: #FFFBEB;
  --bg-card: rgba(255, 255, 255, 0.85);
  --bg-card-hover: rgba(255, 255, 255, 0.98);
  --bg-gradient-start: #FFFBEB;
  --bg-gradient-end: #FEF9C3;
  
  --border: rgba(180, 83, 9, 0.1);
  --border-hover: rgba(217, 119, 6, 0.3);
  
  --shadow-soft: 0 4px 20px rgba(139, 69, 19, 0.06);
  --shadow-hover: 0 16px 40px rgba(139, 69, 19, 0.15);
  --shadow-card: 0 8px 32px rgba(139, 69, 19, 0.08);
  
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
  background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 50%, #FEFCE8 100%);
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

.page-background::after {
  content: '';
  position: absolute;
  bottom: -10%;
  left: -10%;
  width: 40%;
  height: 40%;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.15) 0%, transparent 60%);
  animation: floatGlow 12s ease-in-out infinite reverse;
}

@keyframes floatGlow {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.6; }
  50% { transform: translate(30px, -30px) scale(1.1); opacity: 0.8; }
}

/* ===== 头部区域 ===== */
.gallery-header {
  text-align: center;
  margin-bottom: 3rem;
  animation: fadeIn 0.8s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.header-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 4px 8px rgba(139, 69, 19, 0.2));
}

.gallery-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.gallery-subtitle {
  color: var(--text-sub);
  font-size: 1.125rem;
  margin: 0;
}

/* ===== 卡片网格 ===== */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.75rem;
}

.resume-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 1.75rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}

.resume-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--primary-light), var(--primary));
  background-size: 200% 100%;
  opacity: 0;
  transition: opacity 0.3s ease;
  animation: shimmer 3s linear infinite;
}

.resume-card::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, var(--primary-glow) 0%, transparent 70%);
  opacity: 0;
  transform: scale(0);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.resume-card:hover {
  transform: translateY(-8px) scale(1.01);
  border-color: var(--border-hover);
  box-shadow: var(--shadow-hover);
  background: var(--bg-card-hover);
}

.resume-card:hover::before {
  opacity: 1;
}

.resume-card:hover::after {
  opacity: 0.5;
  transform: scale(1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, #fcd34d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 6px 20px rgba(217, 119, 6, 0.3);
  position: relative;
  transition: transform 0.3s ease;
}

.avatar::before {
  content: '';
  position: absolute;
  top: 8%;
  left: 15%;
  width: 30%;
  height: 30%;
  background: rgba(255, 255, 255, 0.35);
  border-radius: 50%;
  transform: rotate(-30deg);
}

.resume-card:hover .avatar {
  transform: scale(1.05);
}

.header-info .name {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
}

.header-info .role {
  margin: 4px 0 0;
  font-size: 0.875rem;
  color: var(--text-muted);
}

.card-body {
  padding: 0.5rem 0;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  color: var(--text-sub);
}

.info-icon {
  color: var(--text-muted);
  font-size: 1rem;
}

.skills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

/* Element Plus 标签暖色适配 */
:deep(.el-tag--warning.el-tag--plain) {
  background: rgba(217, 119, 6, 0.08);
  border-color: rgba(217, 119, 6, 0.15);
  color: var(--primary-dark);
  border-radius: var(--radius-sm);
  padding: 0.25rem 0.625rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

:deep(.el-tag--warning.el-tag--plain:hover) {
  background: rgba(217, 119, 6, 0.15);
  border-color: rgba(217, 119, 6, 0.3);
  transform: translateY(-1px);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
  margin-top: 0.75rem;
}

.lock-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--text-muted);
  background: rgba(139, 69, 19, 0.05);
  padding: 0.25rem 0.6rem;
  border-radius: 0.5rem;
}

/* Element Plus 按钮暖色适配 */
:deep(.el-button--warning) {
  background: linear-gradient(135deg, rgba(217, 119, 6, 0.12) 0%, rgba(245, 158, 11, 0.08) 100%);
  border-color: rgba(217, 119, 6, 0.25);
  color: var(--primary-dark);
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.el-button--warning:hover) {
  background: linear-gradient(135deg, rgba(217, 119, 6, 0.25) 0%, rgba(245, 158, 11, 0.15) 100%);
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.25);
}

:deep(.el-button--warning:active) {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(217, 119, 6, 0.2);
}

/* ===== 对话框样式 ===== */
.warm-dialog {
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(139, 69, 19, 0.15);
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, var(--bg-card) 0%, rgba(254, 243, 199, 0.5) 100%);
  border-bottom: 1px solid var(--border);
  padding: 1.5rem;
}

:deep(.el-dialog__title) {
  color: var(--text-main);
  font-weight: 700;
  font-size: 1.125rem;
}

:deep(.el-dialog__body) {
  padding: 2rem 1.5rem;
  background: var(--bg-page);
}

:deep(.el-dialog__footer) {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, rgba(254, 243, 199, 0.5) 0%, var(--bg-card) 100%);
  border-top: 1px solid var(--border);
}

:deep(.el-dialog__close) {
  color: var(--text-muted);
  transition: all 0.2s ease;
}

:deep(.el-dialog__close:hover) {
  color: var(--primary);
  transform: rotate(90deg);
}

.dialog-content {
  text-align: center;
}

.dialog-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, #fcd34d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 auto 1.25rem;
  box-shadow: 0 8px 24px rgba(217, 119, 6, 0.35);
  position: relative;
  transition: transform 0.3s ease;
}

.dialog-avatar::before {
  content: '';
  position: absolute;
  top: 10%;
  left: 15%;
  width: 25%;
  height: 25%;
  background: rgba(255, 255, 255, 0.35);
  border-radius: 50%;
  transform: rotate(-30deg);
}

.warm-dialog:hover .dialog-avatar {
  transform: scale(1.05);
}

.dialog-title {
  font-size: 0.95rem;
  color: var(--text-sub);
  margin-bottom: 1.5rem;
}

.dialog-title strong {
  color: var(--text-main);
}

/* 输入框暖色适配 */
:deep(.warm-input .el-input__wrapper) {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 250, 235, 0.8) 100%);
  box-shadow: 0 0 0 1px var(--border) inset, 0 2px 8px rgba(139, 69, 19, 0.04);
  border-radius: var(--radius-lg);
  padding: 0.875rem 1.25rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.warm-input .el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px var(--primary) inset, 0 0 20px rgba(217, 119, 6, 0.15);
  border-color: var(--primary);
}

:deep(.warm-input .el-input__inner) {
  color: var(--text-main);
  font-size: 1rem;
  font-weight: 500;
}

:deep(.warm-input .el-input__suffix) {
  color: var(--text-muted);
  transition: color 0.2s ease;
}

:deep(.warm-input.is-focus .el-input__suffix) {
  color: var(--primary);
}

.error-msg {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.75rem;
  background: rgba(239, 68, 68, 0.08);
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* ===== 响应式适配 ===== */
@media (max-width: 768px) {
  .resume-gallery { padding: 90px 1rem 3rem; }
  .card-grid { grid-template-columns: 1fr; }
  .gallery-title { font-size: 1.875rem; }
  :deep(.el-dialog) { width: 90% !important; }
}
</style>