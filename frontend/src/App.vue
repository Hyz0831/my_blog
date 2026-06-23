<script setup lang="ts">
import Navbar from './components/Navbar.vue'
import PoliceFilingBadge from './components/PoliceFilingBadge.vue'
import beianIcon from './assets/备案图标.png'
</script>

<template>
  <div id="app">
    <Navbar />
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>
    
    <footer class="site-footer">
      <div class="footer-content">
        <div class="footer-info">
          <p class="footer-title">Kang的博客</p>
          <p class="footer-desc">记录技术成长，分享学习心得</p>
        </div>
        <div class="filing-group">
          <PoliceFilingBadge
              record-number="豫公网安备41019702004639号"
              record-code="41019702004639"
              :image-url="beianIcon"
              href="https://beian.mps.gov.cn/#/query/webSearch?recordcode=41019702004639"
          />
          <a
              href="https://beian.miit.gov.cn/"
              target="_blank"
              rel="noopener noreferrer"
              class="icp-link"
          >
            豫ICP备2026013524号
          </a>
        </div>
        <p class="copyright">© 2026 MyBlog. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.app-main {
  flex: 1;
  width: 100%;
  position: relative;
  z-index: 1;
}

.site-footer {
  display: flex;
  justify-content: center;
  padding: var(--spacing-2xl) 0;
  margin-top: auto;
  position: relative;
  z-index: 1;
}

.footer-content {
  width: 100%;
  max-width: 1200px;
  padding: 0 var(--spacing-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
}

.footer-info {
  text-align: center;
}

.footer-title {
  font-size: var(--font-xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.footer-desc {
  font-size: var(--font-sm);
  color: var(--text-muted);
}

.filing-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
}

.icp-link {
  font-size: var(--font-xs);
  color: var(--text-disabled);
}

.copyright {
  font-size: var(--font-xs);
  color: var(--text-disabled);
  margin-top: var(--spacing-sm);
}

/* 页面切换过渡 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all var(--transition-normal);
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
