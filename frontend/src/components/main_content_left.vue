<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Calendar from './Calendar.vue'

// 定义社交图标接口
interface SocialIcon {
  name: string
  url: string
  src: string
  visible: boolean
}

// 使用 import.meta.url 正确引用静态资源
const socialIcons = ref<SocialIcon[]>([
  { 
    name: 'GitHub', 
    url: 'https://github.com', 
    src: new URL('../assets/github.svg', import.meta.url).href, 
    visible: false 
  },
  { 
    name: 'Bilibili', 
    url: 'https://bilibili.com', 
    src: new URL('../assets/bilibili.svg', import.meta.url).href, 
    visible: false 
  },
  { 
    name: 'Twitter', 
    url: 'https://twitter.com', 
    src: new URL('../assets/telegram.svg', import.meta.url).href, // 假设用 telegram 图标代替或替换为 twitter.svg
    visible: false 
  },
  { 
    name: 'Email', 
    url: 'mailto:your@email.com', 
    src: new URL('../assets/douyin.svg', import.meta.url).href, // 建议替换为 email.svg
    visible: false 
  }
])

// 封面图
const bannerImg = new URL('../assets/preview.jpg', import.meta.url).href
// 头像 (建议替换为真实头像)
const avatarImg = new URL('../assets/404.svg', import.meta.url).href

// 入场动画逻辑
onMounted(() => {
  socialIcons.value.forEach((icon, index) => {
    setTimeout(() => {
      icon.visible = true
    }, 300 + index * 100)
  })
})
</script>

<template>
  <div class="sidebar-container">
    <!-- 个人资料卡片 -->
    <article class="glass-card profile-card">
      <!-- 顶部Banner -->
      <div class="banner-wrapper">
        <img :src="bannerImg" alt="Banner" class="banner-img" loading="lazy" />
        <div class="banner-overlay"></div>
      </div>

      <!-- 个人信息区 -->
      <div class="profile-body">
        <div class="avatar-container">
          <img :src="avatarImg" alt="Avatar" class="avatar" />
          <div class="avatar-status"></div>
        </div>
        
        <h2 class="nickname">黄玉宗</h2>
        <p class="signature">Full Stack Developer | AI Enthusiast</p>
        
        <!-- 统计数据 -->
        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-value">42</span>
            <span class="stat-label">文章</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">12k</span>
            <span class="stat-label">阅读</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">365</span>
            <span class="stat-label">天数</span>
          </div>
        </div>

        <!-- 社交链接 -->
        <div class="social-links">
          <a 
            v-for="icon in socialIcons" 
            :key="icon.name"
            :href="icon.url" 
            target="_blank"
            class="social-icon-btn"
            :class="{ 'fade-in': icon.visible }"
            :aria-label="icon.name"
          >
            <img :src="icon.src" :alt="icon.name" class="social-svg" />
          </a>
        </div>
      </div>
    </article>

    <!-- 日历/时间轨迹卡片 -->
    <article class="glass-card calendar-widget">
      <div class="widget-header">
        <span class="widget-title">⏰ 时间轨迹</span>
      </div>
      <div class="widget-content">
        <Calendar />
      </div>
    </article>
  </div>
</template>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

/* 通用玻璃卡片样式 */
.glass-card {
  background: rgba(30, 41, 59, 0.4); /* Slate-800 with opacity */
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.glass-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
  border-color: rgba(99, 102, 241, 0.3); /* Primary color hint */
}

/* --- 个人资料卡片 --- */
.banner-wrapper {
  position: relative;
  height: 120px;
  width: 100%;
  overflow: hidden;
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.glass-card:hover .banner-img {
  transform: scale(1.05);
}

.banner-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(15, 23, 42, 0.8) 100%);
}

.profile-body {
  padding: 0 1.5rem 1.5rem;
  text-align: center;
  position: relative;
}

.avatar-container {
  position: relative;
  width: 90px;
  height: 90px;
  margin: -45px auto 1rem; /* 向上偏移，覆盖 Banner */
  padding: 3px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #1e293b; /* 与背景色一致 */
  background-color: #1e293b;
}

.nickname {
  font-size: 1.25rem;
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 0.25rem;
}

.signature {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

/* 统计数据 */
.stats-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 0.75rem 0;
  margin-bottom: 1.25rem;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #f1f5f9;
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
}

.stat-divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.1);
}

/* 社交图标 */
.social-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.social-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  transform: translateY(10px);
}

.social-icon-btn.fade-in {
  opacity: 1;
  transform: translateY(0);
}

.social-icon-btn:hover {
  background: rgba(99, 102, 241, 0.2);
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.social-svg {
  width: 18px;
  height: 18px;
  filter: invert(1) opacity(0.7); /* 将黑色 SVG 变为白色 */
  transition: filter 0.3s ease;
}

.social-icon-btn:hover .social-svg {
  filter: invert(1) opacity(1) drop-shadow(0 0 4px rgba(255, 255, 255, 0.5));
}

/* --- 日历小组件 --- */
.widget-header {
  padding: 1rem 1.5rem 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.widget-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.widget-content {
  padding: 1rem;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .banner-wrapper {
    height: 100px;
  }
  
  .avatar-container {
    width: 80px;
    height: 80px;
    margin-top: -40px;
  }
  
  .stats-row {
    padding: 0.5rem 0;
  }
  
  .stat-value {
    font-size: 1rem;
  }
}
</style>