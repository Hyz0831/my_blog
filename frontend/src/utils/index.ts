export function debounce<T extends (...args: unknown[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout> | null = null
  return function (this: unknown, ...args: Parameters<T>) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

export function throttle<T extends (...args: unknown[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let lastTime = 0
  return function (this: unknown, ...args: Parameters<T>) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}

export function formatDate(dateStr: string, format: string = 'YYYY-MM-DD'): string {
  if (!dateStr) return '-'
  
  const date = new Date(dateStr.replace(' ', 'T'))
  if (isNaN(date.getTime())) return '-'
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
}

export function truncateText(text: string, maxLength: number = 100): string {
  if (!text || text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

const TAG_SEPARATOR_PATTERN = /[,;，；|/\\]+/
const MAX_TAG_LENGTH = 20
const MAX_TAGS_COUNT = 10

type TagInput = string | string[] | null | undefined

export function normalizeTags(tags: TagInput): string[] {
  if (!tags) return []
  
  let raw: string[] = []
  
  if (Array.isArray(tags)) {
    raw = tags.map(t => String(t).trim()).filter(Boolean)
  } else if (typeof tags === 'string') {
    const trimmed = tags.trim()
    if (!trimmed) return []
    
    if (trimmed.startsWith('[') || trimmed.startsWith('{')) {
      try {
        const parsed = JSON.parse(trimmed)
        raw = Array.isArray(parsed) ? parsed : [String(parsed)]
      } catch {
        raw = splitBySeparators(trimmed)
      }
    } else {
      raw = splitBySeparators(trimmed)
    }
  }
  
  const processed = raw
    .map(tag => sanitizeTag(tag))
    .filter(tag => tag.length > 0 && tag.length <= MAX_TAG_LENGTH)
    .filter((tag, index, arr) => arr.indexOf(tag) === index)
    .slice(0, MAX_TAGS_COUNT)
  
  return processed
}

function splitBySeparators(str: string): string[] {
  return str
    .split(TAG_SEPARATOR_PATTERN)
    .map(s => s.trim())
    .filter(s => s.length > 0)
}

function sanitizeTag(tag: string): string {
  return tag
    .replace(/[\r\n\t]/g, ' ')
    .replace(/\s{2,}/g, ' ')
    .trim()
}

export function getPrimaryTag(tags: TagInput): string {
  const normalized = normalizeTags(tags)
  return normalized[0] || '未分类'
}

export function getTagColor(tag: string): string {
  const colors = [
    '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
    '#00CED1', '#FF69B4', '#9370DB', '#20B2AA', '#FF7F50'
  ]
  let hash = 0
  for (let i = 0; i < tag.length; i++) {
    hash = tag.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length]
}

export function filterMarkdown(text?: string): string {
  if (!text || typeof text !== 'string') return ''

  return text
    .replace(/```[\s\S]*?```/g, '[代码块]')          // 代码块
    .replace(/`[^`\n]+`/g, '')                          // 行内代码
    .replace(/!\[.*?\]\(.*?\)/g, '[图片]')              // 图片
    .replace(/\[.*?\]\(.*?\)/g, '$1')                   // 链接保留文字
    .replace(/^#{1,6}\s+/gm, '')                        // 标题标记
    .replace(/\*{1,3}(.+?)\*{1,3}/g, '$1')             // 加粗/斜体
    .replace(/~~(.+?)~~/g, '$1')                        // 删除线
    .replace(/^\s*>+\s?/gm, '')                         // 引用块
    .replace(/^\s*[-*+]\s+/gm, '')                      // 无序列表
    .replace(/^\s*\d+\.\s+/gm, '')                      // 有序列表
    .replace(/\n{2,}/g, '\n')                           // 多余空行
    .replace(/\|[-:|]+\|/g, '')                         // 表格分隔线
    .replace(/^\|.+\|$/gm, (m) => m.replace(/\|/g, ' ').trim()) // 表格行
    .replace(/---+/g, '')                               // 分割线
    .replace(/&nbsp;/g, ' ')                            // HTML 实体
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .trim()
}

export function getRelativeTime(dateStr: string): string {
  if (!dateStr) return '-'
  
  const date = new Date(dateStr.replace(' ', 'T'))
  if (isNaN(date.getTime())) return '-'
  
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour
  const week = 7 * day
  const month = 30 * day
  const year = 365 * day
  
  if (diff < minute) return '刚刚'
  if (diff < hour) return `${Math.floor(diff / minute)}分钟前`
  if (diff < day) return `${Math.floor(diff / hour)}小时前`
  if (diff < week) return `${Math.floor(diff / day)}天前`
  if (diff < month) return `${Math.floor(diff / week)}周前`
  if (diff < year) return `${Math.floor(diff / month)}个月前`
  
  return `${Math.floor(diff / year)}年前`
}