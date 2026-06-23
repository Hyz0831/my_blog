<script setup lang="ts">
import Resume_Detail from './Resume_Detail.vue'

// 定义组件属性
const props = defineProps({
  resumes: {
    type: Array as () => Array<{
      name: string;
      path: string;
      filename: string;
      description: string;
      icon: string;
    }>,
    default: () => []
  },
  isAuthenticated: {
    type: Boolean,
    default: false
  },
  currentResume: {
    type: Object as () => {
      name: string;
      path: string;
      filename: string;
      description: string;
      icon: string;
    } | null,
    default: null
  }
})

// 定义事件
const emit = defineEmits(['view', 'download', 'select'])

// 处理查看详情
const handleView = (resume: any) => {
  emit('view', resume)
}

// 处理下载
const handleDownload = (resume: any) => {
  emit('download', resume)
}

// 处理选择简历
const handleSelect = (resume: any) => {
  emit('select', resume)
}
</script>

<template>
  <div class="resume-list">
    <div class="resume-cards">
      <div 
        v-for="(resume, index) in resumes" 
        :key="index"
        class="resume-card-wrapper"
      >
        <Resume_Detail 
          :resume="resume"
          :isAuthenticated="isAuthenticated"
          @view="handleView"
          @download="handleDownload"
          @select="handleSelect"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.resume-list {
  width: 100%;
}

.resume-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  margin: 40px 0;
  width: 100%;
  max-width: 1200px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .resume-cards {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>