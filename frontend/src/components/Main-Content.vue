<script setup lang="ts">
import LeftContent from './main_content_left.vue'
import MainContainer from './main_container.vue'
</script>

<template>
  <div class="page-layout">
    <div class="layout-grid">
      <!-- 左侧边栏：个人简介、导航、标签等 -->
      <aside class="sidebar-column">
        <div class="sticky-wrapper">
          <LeftContent />
        </div>
      </aside>

      <!-- 右侧主内容：文章列表、详情等 -->
      <main class="content-column">
        <div class="glass-card">
          <MainContainer />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* 布局容器 */
.page-layout {
  width: 100%;
  min-height: calc(100vh - 70px); /* 减去导航栏高度 */
  display: flex;
  justify-content: center;
  padding-top: 2rem; /* 顶部留白 */
  padding-bottom: 4rem; /* 底部留白 */
}

.layout-grid {
  display: grid;
  /* 侧边栏固定最小宽度，主内容自适应 */
  grid-template-columns: 300px 1fr; 
  gap: 2rem;
  width: 90%;
  max-width: 1280px;
}

/* 侧边栏列 */
.sidebar-column {
  /* 确保侧边栏在移动端堆叠时占满宽度 */
  width: 100%;
}

.sticky-wrapper {
  position: sticky;
  top: 90px; /* 距离顶部的距离，避开导航栏 */
  max-height: calc(100vh - 120px); /* 防止过高溢出屏幕 */
  overflow-y: auto; /* 如果侧边栏内容过多，允许内部滚动 */
  
  /* 隐藏滚动条但保留功能 */
  scrollbar-width: none; 
  -ms-overflow-style: none;
}

.sticky-wrapper::-webkit-scrollbar {
  display: none;
}

/* 主内容列 */
.content-column {
  width: 100%;
  min-width: 0; /* 防止子元素溢出 Grid 单元格 */
}

/* 玻璃拟态卡片容器 */
.glass-card {
  background: rgba(30, 41, 59, 0.4); /* 半透明深色背景 */
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  
  /* 确保内容最小高度，避免看起来太短 */
  min-height: 600px;
}

/* 响应式设计 */

/* 中等屏幕 (平板/小笔记本) */
@media (max-width: 1024px) {
  .layout-grid {
    grid-template-columns: 260px 1fr;
    gap: 1.5rem;
    width: 95%;
  }
  
  .glass-card {
    padding: 1.5rem;
  }
}

/* 小屏幕 (手机/大手机) */
@media (max-width: 768px) {
  .page-layout {
    padding-top: 1rem;
  }

  .layout-grid {
    grid-template-columns: 1fr; /* 单列布局 */
    gap: 1.5rem;
    width: 95%;
  }

  .sidebar-column {
    order: -1; /* 确保侧边栏在移动端显示在内容上方 (如果需要) */
  }

  .sticky-wrapper {
    position: static; /* 移动端取消 sticky，避免占用过多视口 */
    max-height: none;
    overflow-y: visible;
  }
  
  /* 移动端侧边栏样式微调 */
  :deep(.left-content) {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(16px);
  }

  .glass-card {
    padding: 1.25rem;
    border-radius: 12px;
    min-height: auto;
  }
}
</style>