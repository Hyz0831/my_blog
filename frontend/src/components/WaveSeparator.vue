<script setup lang="ts">
import { ref } from 'vue'
// 如果你有 API 文件，可以取消注释下面这行来启用真实数据
// import { get_data_count } from '../api/test'



// --- 1. 粒子配置 ---
const particleCount = 30
const particles = Array.from({ length: particleCount }).map((_, i) => ({
  id: i,
  left: `${Math.random() * 100}%`,
  top: `${Math.random() * 100}%`,
  delay: `${Math.random() * 5}s`,
  duration: `${4 + Math.random() * 4}s`,
  size: `${2 + Math.random() * 3}px`
}))

// --- 2. 波浪路径数据 ---
const wavePaths = [
  "M0,64 C480,150 720,0 1200,64 L1200,120 L0,120 Z", // 平缓
  "M0,80 C300,10 900,110 1200,80 L1200,120 L0,120 Z", // 起伏
  "M0,100 C600,140 800,60 1200,100 L1200,120 L0,120 Z" // 细微
]

// --- 3. 统计数据 (支持动态更新) ---
const stats = ref({
  texts_count: 42,
  read_count: 12000,
  customer_count: 100
})

// 数字格式化函数 (例如: 12000 -> 12.0k+)
const formatNumber = (num: number): string => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w+'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k+'
  }
  return num.toString() + '+'
}

// --- 4. 交互逻辑 ---
const scrollToContent = () => {
  window.scrollTo({
    top: window.innerHeight,
    behavior: 'smooth'
  })
}

// 如果需要从后端获取真实数据，取消注释以下代码
/*
onMounted(async () => {
  try {
    const res = await get_data_count()
    if (res.code === 200 && res.data) {
      stats.value = res.data
    }
  } catch (e) {
    console.warn('Failed to fetch hero stats, using defaults.')
  }
})
*/
</script>

<template>
  <section class="hero-section">
    <!-- 1. 背景特效层 -->
    <div class="hero-bg-effects">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>

    <!-- 2. 粒子层 -->
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

    <!-- 3. 内容层 -->
    <div class="hero-content">
      <div class="hero-badge fade-in-up" style="animation-delay: 0.1s;">
        <span class="badge-dot"></span>
        欢迎来到我的博客
      </div>

      <h1 class="hero-title fade-in-up" style="animation-delay: 0.2s;">
        <span class="title-line">探索技术的</span>
        <span class="title-gradient">无限可能</span>
      </h1>

      <p class="hero-subtitle fade-in-up" style="animation-delay: 0.3s;">
        记录成长轨迹，分享技术心得，与志同道合者同行
      </p>

      <!-- 动态统计数据 -->
      <div class="hero-stats fade-in-up" style="animation-delay: 0.4s;">
        <div class="stat-item">
          <span class="stat-number">{{ formatNumber(stats.texts_count) }}</span>
          <span class="stat-label">篇文章</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">{{ formatNumber(stats.read_count) }}</span>
          <span class="stat-label">阅读量</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">{{ formatNumber(stats.customer_count) }}</span>
          <span class="stat-label">访客</span>
        </div>
      </div>

      <div class="hero-actions fade-in-up" style="animation-delay: 0.5s;">
        <router-link to="/posts" class="hero-btn primary">
          <span class="btn-content">
            <span class="btn-text">开始阅读</span>
            <svg class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </span>
          <span class="btn-glow"></span>
        </router-link>
        <router-link to="/about" class="hero-btn secondary">
          <span class="btn-text">了解更多</span>
        </router-link>
      </div>
    </div>

    <!-- 4. 波浪分隔层 (纯 CSS 动画) -->
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

    <!-- 5. 滚动提示 -->
    <div
        class="scroll-indicator fade-in-up"
        style="animation-delay: 0.8s;"
        @click="scrollToContent"
        role="button"
        aria-label="滚动到主要内容"
        tabindex="0"
        @keydown.enter="scrollToContent"
    >
      <div class="mouse">
        <div class="wheel"></div>
      </div>
      <span class="scroll-text">向下滚动</span>
    </div>
  </section>
</template>

<style scoped>
/* ===== 变量定义 - 暖色系 ===== */
.hero-section {
  --primary-color: #d97706; /* Amber-600 */
  --secondary-color: #b45309; /* Amber-700 */
  --accent-color: #f59e0b; /* Amber-500 */
  --text-primary: #451a03; /* Deep Brown */
  --text-secondary: #78350f; /* Medium Brown */
  --bg-light: #FFFBEB; /* Amber-50 */

  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(180deg, #FFFBEB 0%, #FEF3C7 100%);
  padding-top: 60px; /* 避开固定导航栏 */
}

/* ===== 1. 背景特效 ===== */
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
  will-change: transform; /* 性能优化 */
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

/* ===== 2. 粒子效果 ===== */
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
  0% {
    opacity: 0;
    transform: translateY(0) scale(0);
  }
  20% {
    opacity: 0.8;
    transform: translateY(-20px) scale(1);
  }
  80% {
    opacity: 0.5;
  }
  100% {
    opacity: 0;
    transform: translateY(-100px) scale(0.5);
  }
}

/* ===== 3. 内容层 ===== */
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
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  margin-left: auto;
  margin-right: auto;
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

/* ===== 4. 波浪动画 (CSS Only) ===== */
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
  width: 200%; /* 加宽以便移动 */
  height: 100%;
}

.wave-1 {
  animation: waveMove 15s linear infinite;
  opacity: 0.8;
}

.wave-2 {
  animation: waveMove 20s linear infinite reverse;
  opacity: 0.6;
  bottom: 10px;
}

.wave-3 {
  animation: waveMove 25s linear infinite;
  opacity: 0.4;
  bottom: 20px;
}

@keyframes waveMove {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ===== 5. 滚动指示器 ===== */
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
  transition: opacity 0.3s;
}

.scroll-indicator:hover {
  opacity: 0.8;
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
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* ===== 响应式适配 ===== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-stats {
    gap: 1rem;
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
    display: none; /* 移动端通常不需要滚动提示，或者可以保留 */
  }
}
</style>