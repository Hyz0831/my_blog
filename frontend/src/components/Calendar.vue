<template>
  <div class="time-card">
    <div class="time-content">
      <div class="time-display">{{ time }}</div>
      <div class="date-display">{{ date }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const time = ref('')
const date = ref('')

const updateTime = () => {
  const now = new Date()

  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  time.value = `${hours}:${minutes}:${seconds}`

  const year = now.getFullYear()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const weekday = weekdays[now.getDay()]
  date.value = `${year}年${month}月${day}日 · ${weekday}`
}

let timer: number | null = null

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.time-card {
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all var(--transition-normal);
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
}

.time-card:hover {
  transform: translateY(-3px);
  border-color: rgba(99, 102, 241, 0.3);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
}

.time-content {
  padding: var(--spacing-xl);
  text-align: center;
}

.time-display {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--color-primary-light);
  margin-bottom: var(--spacing-sm);
  font-family: 'Courier New', Consolas, monospace;
  letter-spacing: 2px;
}

.date-display {
  font-size: var(--font-sm);
  color: var(--text-muted);
  font-weight: 500;
}

@media (max-width: 768px) {
  .time-display {
    font-size: 1.8rem;
  }
}

@media (max-width: 480px) {
  .time-display {
    font-size: 1.5rem;
  }

  .time-card {
    max-width: none;
  }
}
</style>
