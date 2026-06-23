<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Menu, Close } from '@element-plus/icons-vue'

interface NavItem {
  name: string
  path: string
}

const route = useRoute()
const isMenuOpen = ref(false)
const isScrolled = ref(false)

// 保持原有的导航类别
const navItems: NavItem[] = [
  { name: '首页', path: '/' },
  { name: '主页', path: '/home' },
  { name: '文章', path: '/posts' },
  { name: '资源仓库', path: '/resources' },
  { name: '关于', path: '/about' },
]

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
  document.body.style.overflow = isMenuOpen.value ? 'hidden' : ''
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

watch(() => route.path, () => {
  if (isMenuOpen.value) {
    toggleMenu()
  }
})

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.body.style.overflow = ''
})
</script>

<template>
  <header class="navbar-wrapper" :class="{ 'scrolled': isScrolled }">
    <nav class="top-navbar">
      <!-- 顶部暖色流光线条 -->
      <div class="navbar-glow"></div>
      
      <div class="navbar-container">
        <!-- Logo 区域 -->
        <router-link to="/" class="navbar-brand">
          <div class="brand-icon">
            <span class="brand-letter">K</span>
          </div>
          <div class="brand-text-group">
            <span class="brand-name">Kang的博客</span>
            <span class="brand-dot">.</span>
          </div>
        </router-link>

        <!-- 导航菜单 -->
        <ul class="navbar-menu" :class="{ 'active': isMenuOpen }">
          <li v-for="item in navItems" :key="item.path" class="nav-item">
            <router-link
              :to="item.path"
              class="nav-link"
              active-class="router-link-active"
              @click="toggleMenu"
            >
              <span class="nav-text">{{ item.name }}</span>
              <span class="nav-indicator"></span>
            </router-link>
          </li>
        </ul>

        <!-- 移动端切换按钮 -->
        <button
          class="navbar-toggle"
          :class="{ 'open': isMenuOpen }"
          @click="toggleMenu"
          aria-label="Toggle navigation"
        >
          <Menu v-if="!isMenuOpen" :size="24" />
          <Close v-else :size="24" />
        </button>
      </div>
    </nav>
    
    <!-- 移动端遮罩层 -->
    <div 
      class="mobile-overlay" 
      :class="{ 'visible': isMenuOpen }"
      @click="toggleMenu"
    ></div>
  </header>
</template>

<style scoped>
/* 暖色系变量定义 */
.navbar-wrapper {
  --nav-height: 70px;
  
  /* 暖色主色调：琥珀色/焦糖色 */
  --color-primary: #d97706;   /* Amber-600 */
  --color-secondary: #b45309; /* Amber-700 */
  --color-accent: #f59e0b;    /* Amber-500 */
  
  /* 文字颜色：深棕色，比纯黑更柔和 */
  --text-primary: #433422;    /* Warm Dark Brown */
  --text-secondary: #785c46;  /* Medium Brown */
  
  /* 背景色：暖白色/米色 */
  --bg-glass: rgba(255, 250, 240, 0.75); /* FloralWhite with opacity */
  --bg-glass-scrolled: rgba(255, 250, 240, 0.95);
  
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--nav-height);
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.top-navbar {
  width: 100%;
  height: 100%;
  background: var(--bg-glass);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(180, 140, 100, 0.1); /* 暖色边框 */
  position: relative;
  transition: all 0.3s ease;
}

.scrolled .top-navbar {
  background: var(--bg-glass-scrolled);
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08); /* 暖色阴影 */
  border-bottom: 1px solid rgba(180, 140, 100, 0.2);
}

/* 顶部流光线条：暖金色渐变 */
.navbar-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(217, 119, 6, 0.4) 20%, 
    rgba(245, 158, 11, 0.8) 50%, 
    rgba(217, 119, 6, 0.4) 80%, 
    transparent 100%
  );
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.scrolled .navbar-glow {
  opacity: 1;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
}

.navbar-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Brand 样式 */
.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  z-index: 1001;
}

.brand-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 暖色渐变 Logo */
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.25);
  transition: transform 0.2s ease;
}

.brand-letter {
  color: white;
  font-weight: 800;
  font-size: 1.2rem;
  font-family: 'Times New Roman', serif;
}

.navbar-brand:hover .brand-icon {
  transform: rotate(-5deg) scale(1.05);
}

.brand-text-group {
  display: flex;
  align-items: baseline;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.brand-dot {
  color: var(--color-primary);
  font-size: 1.5rem;
  line-height: 0;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

/* 菜单样式 */
.navbar-menu {
  display: flex;
  list-style: none;
  gap: 0.5rem;
  margin: 0;
  padding: 0;
}

.nav-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.95rem;
  position: relative;
  padding: 0.5rem 0.25rem;
  transition: color 0.2s ease;
}

.nav-text {
  position: relative;
  z-index: 1;
}

.nav-indicator {
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: var(--color-primary);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: var(--color-primary);
}

.nav-link:hover .nav-indicator {
  width: 100%;
}

/* 激活状态 */
.router-link-active {
  color: var(--color-primary);
}

.router-link-active .nav-indicator {
  width: 100%;
  box-shadow: 0 0 8px rgba(217, 119, 6, 0.4);
}

/* 移动端按钮 */
.navbar-toggle {
  display: none;
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  z-index: 1001;
}

.navbar-toggle:hover {
  background: rgba(217, 119, 6, 0.1);
}

.mobile-overlay {
  position: fixed;
  inset: 0;
  background: rgba(67, 52, 34, 0.2); /* 暖色遮罩 */
  backdrop-filter: blur(4px);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.mobile-overlay.visible {
  opacity: 1;
  visibility: visible;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .navbar-menu {
    position: fixed;
    top: 0;
    right: 0;
    width: 260px;
    height: 100vh;
    /* 移动端菜单背景：更实的暖白色 */
    background: rgba(255, 253, 245, 0.98);
    backdrop-filter: blur(20px);
    flex-direction: column;
    padding: 5rem 1.5rem 2rem;
    gap: 0.5rem;
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: -5px 0 30px rgba(139, 69, 19, 0.1);
    border-left: 1px solid rgba(180, 140, 100, 0.2);
    z-index: 1000;
  }

  .navbar-menu.active {
    transform: translateX(0);
  }

  .nav-link {
    width: 100%;
    padding: 1rem;
    font-size: 1.05rem;
    flex-direction: row;
    justify-content: space-between;
    border-radius: 8px;
    color: var(--text-secondary);
  }

  .nav-link:hover {
    background: rgba(217, 119, 6, 0.08);
    color: var(--color-primary);
  }
  
  .nav-indicator {
    display: none;
  }

  .router-link-active {
    background: rgba(217, 119, 6, 0.12);
    color: var(--color-primary);
    font-weight: 700;
  }
}
</style>