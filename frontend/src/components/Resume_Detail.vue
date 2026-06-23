<script setup lang="ts">
import { Briefcase, Star, Monitor, Document, Download, Files } from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  resume: {
    type: Object,
    default: () => ({
      name: '',
      path: '',
      filename: '',
      description: '',
      icon: 'Document'
    })
  },
  isAuthenticated: {
    type: Boolean,
    default: false
  }
})

// 定义事件
const emit = defineEmits(['view', 'download', 'select'])

// 下载PDF
const handleDownload = () => {
  emit('download', props.resume)
}

// 查看详情
const handleView = () => {
  emit('view', props.resume)
}

// 选择简历
const handleSelect = () => {
  emit('select', props.resume)
}

// 获取图标组件
const getIconComponent = (iconName: string) => {
  const iconMap: any = {
    'Briefcase': Briefcase,
    'Star': Star,
    'Monitor': Monitor,
    'Document': Document,
    'File': Files
  }
  return iconMap[iconName] || Document
}
</script>

<template>
  <div class="resume-detail">
    <!-- 简历卡片 -->
    <div 
      class="resume-card"
      @click="handleSelect"
    >
      <div class="resume-card-header">
        <div class="resume-icon">
          <el-icon :size="40">
            <component :is="getIconComponent(resume.icon)" />
          </el-icon>
        </div>
        <h3 class="resume-card-title">{{ resume.name }}</h3>
        <p class="resume-card-description">{{ resume.description }}</p>
      </div>
      <div class="resume-card-footer">
        <el-button 
          type="primary" 
          size="small" 
          class="view-button"
          @click.stop="handleView"
          :disabled="!isAuthenticated"
        >
          <el-icon><Files /></el-icon>
          查看详情
        </el-button>
        <el-button 
          type="success" 
          size="small" 
          class="download-button"
          @click.stop="handleDownload"
          :disabled="!isAuthenticated"
        >
          <el-icon><Download /></el-icon>
          下载简历
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.resume-detail {
  width: 100%;
}

.resume-card {
  background: rgba(30, 30, 50, 0.6);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.resume-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
  background: rgba(40, 40, 60, 0.7);
  border-color: rgba(99, 179, 237, 0.3);
}

.resume-card-header {
  margin-bottom: 20px;
  text-align: center;
  flex: 1;
}

.resume-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #63b3ed, #4299e1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
}

.resume-card-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #e8e8e8;
  margin-bottom: 10px;
}

.resume-card-description {
  color: #a0aec0;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
  flex: 1;
}

.resume-card-footer {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
}

.view-button {
  background: linear-gradient(135deg, #63b3ed, #4299e1);
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.view-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #4299e1, #3182ce);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 179, 237, 0.4);
}

.download-button {
  background: linear-gradient(135deg, #48bb78, #38a169);
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.download-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #38a169, #2f855a);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(72, 187, 120, 0.4);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .resume-card {
    padding: 20px;
  }
  
  .resume-card-footer {
    flex-direction: column;
  }
  
  .resume-card-footer .el-button {
    width: 100%;
  }
}
</style>