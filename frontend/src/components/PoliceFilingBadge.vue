<template>
  <a
      :href="finalLink"
      target="_blank"
      rel="noopener noreferrer"
      class="police-filing-badge"
      :title="recordNumber"
  >
    <img :src="imageUrl" alt="公安备案标识" class="police-icon" loading="lazy" />
    <span v-if="showText" class="police-text">{{ recordNumber }}</span>
  </a>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** 备案显示文案，如：豫公网安备41019702004639号 */
  recordNumber: { type: String, default: '豫公网安备41019702004639号' },
  /** 备案编号（纯数字），用于自动拼接官方查询链接 */
  recordCode: { type: String, default: '' },
  /** 图标地址，支持网络链接或已导入的本地资源 */
  imageUrl: { type: String, default: 'src/assets/备案图标.png' },
  /** 自定义跳转链接（优先级高于自动拼接） */
  linkUrl: { type: String, default: '' },
  /** 是否显示文字 */
  showText: { type: Boolean, default: true }
})

// 自动生成公安部备案查询链接
const finalLink = computed(() => {
  if (props.linkUrl) return props.linkUrl
  if (props.recordCode) {
    return `https://beian.mps.gov.cn/#/query/webSearch?recordcode=${props.recordCode}`
  }
  return '#'
})
</script>

<style scoped>
.police-filing-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #8c8c8c;
  font-size: 12px;
  line-height: 1;
  text-decoration: none;
  transition: color 0.2s ease;
}

.police-filing-badge:hover {
  color: #595959;
}

.police-icon {
  width: 14px;
  height: 14px;
  object-fit: contain;
  vertical-align: middle;
}

/* 适配深色主题或高对比度场景 */
@media (prefers-color-scheme: dark) {
  .police-filing-badge { color: #a6a6a6; }
  .police-filing-badge:hover { color: #d9d9d9; }
}
</style>