<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <div class="error-code">
        <span class="digit">4</span>
        <span class="digit zero">0</span>
        <span class="digit">4</span>
      </div>
      <h1 class="error-title">页面未找到</h1>
      <p class="error-desc">抱歉，您访问的页面不存在或已被删除</p>
      <div class="error-actions">
        <el-button type="primary" @click="goHome" class="back-btn">
          <el-icon><ArrowLeft /></el-icon>
          返回首页
        </el-button>
      </div>
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
  overflow: hidden;
}

.not-found-content {
  text-align: center;
  padding: var(--spacing-2xl);
  position: relative;
  z-index: 2;
  animation: fadeInUp 0.8s ease forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-code {
  font-size: 10rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: var(--spacing-xl);
  display: flex;
  justify-content: center;
  gap: var(--spacing-sm);
}

.digit {
  color: var(--text-primary);
  opacity: 0.1;
  animation: digitPulse 3s ease-in-out infinite;
}

.digit:nth-child(1) { animation-delay: 0s; }
.digit:nth-child(2) { animation-delay: 0.3s; }
.digit:nth-child(3) { animation-delay: 0.6s; }

.digit.zero {
  opacity: 0.15;
  color: var(--color-primary-light);
  text-shadow: 0 0 40px rgba(99, 102, 241, 0.3);
}

@keyframes digitPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.error-title {
  font-size: var(--font-3xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.error-desc {
  font-size: var(--font-lg);
  color: var(--text-muted);
  margin-bottom: var(--spacing-2xl);
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.error-actions {
  margin-top: var(--spacing-xl);
}

.back-btn {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  border: none;
  padding: var(--spacing-md) var(--spacing-2xl);
  font-size: var(--font-base);
  border-radius: var(--radius-lg);
  transition: all var(--transition-normal);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
}

.back-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
}

.floating-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: -1;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.05;
}

.shape-1 {
  width: 300px;
  height: 300px;
  background: var(--color-primary);
  top: -100px;
  right: -50px;
  animation: float1 8s ease-in-out infinite;
}

.shape-2 {
  width: 200px;
  height: 200px;
  background: var(--color-secondary);
  bottom: -50px;
  left: -30px;
  animation: float2 10s ease-in-out infinite;
}

.shape-3 {
  width: 150px;
  height: 150px;
  background: var(--color-accent);
  top: 50%;
  left: -80px;
  animation: float3 12s ease-in-out infinite;
}

.shape-4 {
  width: 100px;
  height: 100px;
  background: var(--color-primary-light);
  bottom: 20%;
  right: -40px;
  animation: float1 9s ease-in-out infinite reverse;
}

@keyframes float1 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(20px, -20px) rotate(10deg); }
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(-15px, 15px) rotate(-10deg); }
}

@keyframes float3 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(10px, 25px) rotate(5deg); }
}

@media (max-width: 768px) {
  .error-code {
    font-size: 6rem;
  }

  .error-title {
    font-size: var(--font-2xl);
  }

  .error-desc {
    font-size: var(--font-base);
  }
}
</style>
