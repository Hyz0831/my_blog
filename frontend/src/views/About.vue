<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { 
  Share, 
  Message, 
  Link as LinkIcon, 
  Operation, 
  Monitor, 
  DataAnalysis, 
  Menu, 
  Star 
} from '@element-plus/icons-vue'
import { get_profile } from '@/api/api'
import type { ProfileInfo } from '@/api/api'

const profile = ref<ProfileInfo | null>(null)
const loading = ref(true)

const defaultProfile: ProfileInfo = {
  nickname: 'Kang',
  avatar: '',
  title: '技术爱好者 | 持续学习者',
  subtitle: '全栈开发者',
  bio: '你好！我是一名热爱技术的全栈开发者，专注于前端和后端技术的学习与实践。我喜欢通过代码解决实际问题，不断探索新技术和最佳实践。这个博客是我记录学习心得、分享技术见解的地方，希望能与更多技术爱好者交流。',
  tech_stack: [
    { category: '前端技术', items: ['Vue 3 + Composition API', 'TypeScript', 'Element Plus', 'Vite', 'CSS3 / SCSS'] },
    { category: '后端技术', items: ['Python', 'FastAPI', 'SQLite', 'RESTful API'] },
    { category: '工具与其他', items: ['Git', 'VS Code', 'Docker', 'Linux'] }
  ],
  contacts: [
    { platform: 'GitHub', url: '#', icon: 'Share' },
    { platform: 'Email', url: '#', icon: 'Message' },
    { platform: '个人网站', url: '#', icon: 'LinkIcon' }
  ],
  features: [
    { title: '现代化技术栈', description: '使用 Vue 3 + TypeScript 构建，确保代码质量和可维护性', icon: 'Operation' },
    { title: '响应式设计', description: '适配不同设备屏幕，提供良好的移动端体验', icon: 'Menu' },
    { title: '完整的前后端', description: '包含前端展示和后端 API，实现完整的博客功能', icon: 'Monitor' },
    { title: '数据持久化', description: '使用 SQLite 数据库存储文章和用户数据', icon: 'DataAnalysis' }
  ]
}

const loadProfile = async () => {
  loading.value = true
  try {
    const result = await get_profile()
    if (result.code === 200 && result.data) {
      profile.value = result.data
    } else {
      profile.value = defaultProfile
    }
  } catch (error) {
    console.error('加载个人资料失败:', error)
    profile.value = defaultProfile
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<template>
  <div class="about-container">
    <!-- 页面背景 -->
    <div class="page-background"></div>
    
    <div class="about-header">
      <div class="header-icon">
        <el-icon><Star /></el-icon>
      </div>
      <h1 class="about-title">关于我</h1>
      <p class="about-subtitle">技术爱好者 | 持续学习者</p>
    </div>

    <div class="about-content">
      <!-- 个人简介 -->
      <section class="about-section">
        <div class="glass-card">
          <h2 class="section-title">
            <el-icon><Menu /></el-icon>
            个人简介
          </h2>
          <div class="section-content">
            <p>你好！我是一名热爱技术的全栈开发者，专注于前端和后端技术的学习与实践。</p>
            <p>我喜欢通过代码解决实际问题，不断探索新技术和最佳实践。</p>
            <p>这个博客是我记录学习心得、分享技术见解的地方，希望能与更多技术爱好者交流。</p>
          </div>
        </div>
      </section>

      <!-- 技术栈 -->
      <section class="about-section">
        <div class="glass-card">
          <h2 class="section-title">
            <el-icon><Operation /></el-icon>
            技术栈
          </h2>
          <div class="tech-stack">
            <div class="tech-category">
              <h3>前端技术</h3>
              <ul class="tech-list">
                <li>Vue 3 + Composition API</li>
                <li>TypeScript</li>
                <li>Element Plus</li>
                <li>Vite</li>
                <li>CSS3 / SCSS</li>
              </ul>
            </div>
            <div class="tech-category">
              <h3>后端技术</h3>
              <ul class="tech-list">
                <li>Python</li>
                <li>Flask</li>
                <li>SQLite</li>
                <li>RESTful API</li>
              </ul>
            </div>
            <div class="tech-category">
              <h3>工具与其他</h3>
              <ul class="tech-list">
                <li>Git</li>
                <li>VS Code</li>
                <li>Docker</li>
                <li>Linux</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- 项目特点 -->
      <section class="about-section">
        <div class="glass-card">
          <h2 class="section-title">
            <el-icon><Star /></el-icon>
            项目特点
          </h2>
          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon><Operation /></el-icon>
              </div>
              <h3>现代化技术栈</h3>
              <p>使用 Vue 3 + TypeScript 构建，确保代码质量和可维护性</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon><Menu /></el-icon>
              </div>
              <h3>响应式设计</h3>
              <p>适配不同设备屏幕，提供良好的移动端体验</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <h3>完整的前后端</h3>
              <p>包含前端展示和后端 API，实现完整的博客功能</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <el-icon><DataAnalysis /></el-icon>
              </div>
              <h3>数据持久化</h3>
              <p>使用 SQLite 数据库存储文章和用户数据</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 联系方式 -->
      <section class="about-section">
        <div class="glass-card">
          <h2 class="section-title">
            <el-icon><Message /></el-icon>
            联系方式
          </h2>
          <div class="contact-info">
            <a href="#" class="contact-item">
              <el-icon><Share /></el-icon>
              <span>GitHub</span>
            </a>
            <a href="#" class="contact-item">
              <el-icon><Message /></el-icon>
              <span>Email</span>
            </a>
            <a href="#" class="contact-item">
              <el-icon><LinkIcon /></el-icon>
              <span>个人网站</span>
            </a>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ===== 暖色系变量定义 ===== */
.about-container {
  --primary-color: #d97706;      /* Amber-600 */
  --secondary-color: #b45309;    /* Amber-700 */
  --accent-color: #f59e0b;       /* Amber-500 */
  
  --text-primary: #451a03;       /* Deep Brown */
  --text-secondary: #78350f;     /* Medium Brown */
  --text-muted: #92400e;         /* Light Brown */
  
  --bg-page: #FFFBEB;            /* Amber-50 */
  --bg-card: rgba(254, 243, 199, 0.7);  /* Amber-100 with opacity */
  --bg-card-hover: rgba(254, 243, 199, 0.9);
  
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

/* ===== 头部区域 ===== */
.about-header {
  text-align: center;
  margin-bottom: 3rem;
  animation: heroFadeIn 0.8s ease forwards;
}

@keyframes heroFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 暖色渐变背景 */
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  border-radius: 1rem;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 25px rgba(217, 119, 6, 0.3);
}

.header-icon .el-icon {
  font-size: 36px;
  color: white;
}

.about-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.about-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin: 0;
}

/* ===== 内容区域 ===== */
.about-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  gap: 1.5rem;
}

/* 玻璃卡片 */
.glass-card {
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-light);
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: var(--shadow-soft);
  transition: all var(--transition-normal);
}

.glass-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
  border-color: var(--border-hover);
  background: var(--bg-card-hover);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-light);
}

.section-title .el-icon {
  color: var(--primary-color);
  font-size: 1.25rem;
}

.section-content {
  line-height: 1.8;
  color: var(--text-secondary);
  font-size: 1rem;
}

.section-content p {
  margin-bottom: 1rem;
}

.section-content p:last-child {
  margin-bottom: 0;
}

/* ===== 技术栈 ===== */
.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.tech-category h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px dashed var(--border-light);
}

.tech-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-list li {
  padding: 0.5rem 0;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  font-size: 0.95rem;
}

.tech-list li:last-child {
  border-bottom: none;
}

.tech-list li::before {
  content: "▸";
  color: var(--primary-color);
  font-weight: bold;
  margin-right: 0.75rem;
  font-size: 1.1rem;
}

/* ===== 项目特点 ===== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.feature-item {
  text-align: center;
  padding: 1.5rem;
  border-radius: 1rem;
  /* 暖色背景 */
  background: rgba(217, 119, 6, 0.08);
  border: 1px solid var(--border-light);
  transition: all var(--transition-normal);
}

.feature-item:hover {
  transform: translateY(-4px);
  background: rgba(217, 119, 6, 0.15);
  border-color: var(--border-hover);
  box-shadow: var(--shadow-soft);
}

.feature-icon {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.feature-item h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.feature-item p {
  color: var(--text-muted);
  font-size: 0.875rem;
  line-height: 1.6;
}

/* ===== 联系方式 ===== */
.contact-info {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  /* 暖色按钮样式 */
  background: rgba(217, 119, 6, 0.1);
  border: 1px solid rgba(217, 119, 6, 0.2);
  color: var(--text-secondary);
  border-radius: 0.75rem;
  text-decoration: none;
  transition: all var(--transition-normal);
  font-weight: 500;
  font-size: 0.95rem;
}

.contact-item:hover {
  background: rgba(217, 119, 6, 0.2);
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(217, 119, 6, 0.15);
}

.contact-item .el-icon {
  font-size: 1.1rem;
}

/* ===== 响应式适配 ===== */
@media (max-width: 768px) {
  .about-container {
    padding: 90px 1rem 3rem;
  }

  .about-title {
    font-size: 1.875rem;
  }

  .about-subtitle {
    font-size: 1rem;
  }

  .glass-card {
    padding: 1.5rem;
  }

  .tech-stack {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .contact-info {
    flex-direction: column;
    gap: 0.75rem;
  }

  .contact-item {
    justify-content: center;
    width: 100%;
  }
  
  .section-title {
    font-size: 1.125rem;
  }
}

@media (max-width: 480px) {
  .about-title {
    font-size: 1.5rem;
  }
  
  .header-icon {
    width: 64px;
    height: 64px;
  }
  
  .header-icon .el-icon {
    font-size: 28px;
  }
}
</style>