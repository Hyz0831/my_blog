<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { publish_post, edit_post, get_categories, get_text_detail, type PublishPostRequest } from '../api/api'
import type { CategoryItem } from '../api/api'

const router = useRouter()
const isSubmitting = ref(false)
const isEditMode = ref(false)
const currentPostId = ref<number | null>(null)
const coverInputRef = ref<HTMLInputElement>()

// 置顶开关（el-switch 绑定 boolean）
const isTop = ref(false)

// 表单状态
const contentPreview = ref('edit') // 'edit' | 'preview'

const form = reactive({
  title: '',
  content: '',
  content_format: 'markdown',
  summary: '',
  cover_img: '',
  tags: '',
  category_id: undefined as number | undefined,
  visibility: 'public' as 'public' | 'private'
})

// 分类列表
const categories = ref<CategoryItem[]>([])

// 加载分类
const loadCategories = async () => {
  try {
    const result = await get_categories()
    if (result.code === 200) {
      categories.value = result.data
    }
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

// 表单验证
const validateForm = () => {
  if (!form.title.trim()) {
    ElMessage.error('请输入文章标题')
    return false
  }
  if (!form.content.trim()) {
    ElMessage.error('请输入文章内容')
    return false
  }
  return true
}

// 提交表单
const handleSubmit = async () => {
  if (!validateForm()) return

  isSubmitting.value = true
  try {
    const publishData: PublishPostRequest = {
      title: form.title,
      content: form.content,
      content_format: form.content_format,
      summary: form.summary,
      cover_img: form.cover_img,
      tags: form.tags,
      category_id: form.category_id,
      visibility: form.visibility,
      is_top: isTop.value ? 1 : 0
    }

    const result = isEditMode.value
      ? await edit_post(currentPostId.value!, publishData)
      : await publish_post(publishData)

    if (result.code === 200) {
      ElMessage.success(isEditMode.value ? '文章更新成功！' : '文章发布成功！')
      router.push({ path: '/admin', query: { refresh: '1' } })
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error: any) {
    console.error('提交失败:', error)
    ElMessage.error(error.message || '操作失败，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}

// 处理返回
const handleCancel = () => {
  router.push('/admin')
}

// 加载文章详情
const loadPostDetail = async () => {
  const postId = router.currentRoute.value.params.id as string
  if (!postId) return

  try {
    const result = await get_text_detail(postId)
    if (result.code === 200 && result.data) {
      const post = result.data
      form.title = post.title
      form.content = post.content
      form.content_format = post.content_type || 'markdown'
      form.summary = post.summary || ''
      form.cover_img = post.cover_img || ''
      form.tags = Array.isArray(post.tags) ? post.tags.join(',') : (post.tags || '')
      form.category_id = (post as any).category_id || undefined
      form.visibility = post.visibility === 1 ? 'public' : 'private'
      isTop.value = !!(post as any).is_top
    } else {
      ElMessage.error('文章不存在或加载失败')
      router.push('/admin')
    }
  } catch (error) {
    console.error('加载文章详情失败:', error)
    ElMessage.error('加载文章详情失败')
  }
}

// 处理封面上传
const handleCoverUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    form.cover_img = e.target?.result as string
  }
  reader.readAsDataURL(file)
  input.value = ''
}

onMounted(async () => {
  await loadCategories()
  const postId = router.currentRoute.value.params.id as string
  if (postId) {
    currentPostId.value = parseInt(postId)
    isEditMode.value = true
    await loadPostDetail()
  }
})
</script>

<template>
  <div class="publish-container">
    <div class="publish-header">
      <h1 class="page-title">
        <el-icon class="title-icon"><Plus /></el-icon>
        {{ isEditMode ? '编辑文章' : '发布新文章' }}
      </h1>
      <p class="page-subtitle">分享您的技术见解和知识</p>
    </div>

    <div class="publish-content">
      <el-card class="publish-card">
        <el-form :model="form" label-width="80px" label-position="top">
          <!-- 文章标题 -->
          <el-form-item label="文章标题" required>
            <el-input
              v-model="form.title"
              placeholder="请输入文章标题（1-200字）"
              maxlength="200"
              show-word-limit
              size="large"
            />
          </el-form-item>

          <!-- 文章内容 -->
          <el-form-item label="文章内容" required>
            <div class="content-editor-header">
              <el-segmented v-model="contentPreview" :options="[
                { label: '编辑', value: 'edit' },
                { label: '预览', value: 'preview' }
              ]" />
            </div>
            <el-input
              v-if="contentPreview === 'edit'"
              v-model="form.content"
              type="textarea"
              :rows="20"
              placeholder="请输入文章内容（支持 Markdown 格式）"
              maxlength="100000"
              show-word-limit
            />
            <div v-else class="content-preview-area">
              <v-md-preview v-if="form.content" :text="form.content" />
              <el-empty v-else description="暂无内容，请先编辑" />
            </div>
          </el-form-item>

          <!-- 文章摘要 -->
          <el-form-item label="文章摘要">
            <el-input
              v-model="form.summary"
              type="textarea"
              :rows="3"
              placeholder="文章摘要（可选，用于SEO）"
              maxlength="300"
              show-word-limit
            />
          </el-form-item>

          <!-- 封面图片 -->
          <el-form-item label="封面图片">
            <div class="upload-area">
              <el-button
                type="primary"
                :icon="Upload"
                @click="coverInputRef?.click()"
              >
                上传封面
              </el-button>
              <input
                ref="coverInputRef"
                type="file"
                accept="image/*"
                style="display: none"
                @change="handleCoverUpload"
              />
              <span class="upload-tip">支持 JPG、PNG 格式，最大 5MB</span>
            </div>
            <div v-if="form.cover_img" class="cover-preview">
              <el-image :src="form.cover_img" style="width: 200px; height: 120px" fit="cover" />
              <el-button type="danger" size="small" :icon="Upload" circle @click="form.cover_img = ''" />
            </div>
          </el-form-item>

          <!-- 分类 -->
          <el-form-item label="文章分类">
            <el-select
              v-model="form.category_id"
              placeholder="选择分类"
              filterable
              clearable
            >
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.name"
                :value="cat.id"
              />
            </el-select>
          </el-form-item>

          <!-- 标签 -->
          <el-form-item label="文章标签">
            <el-input
              v-model="form.tags"
              placeholder="多个标签用逗号分隔"
              maxlength="100"
              show-word-limit
            />
            <span class="form-tip">使用逗号分隔多个标签，例如：前端,Vue,React</span>
          </el-form-item>

          <!-- 可见性 -->
          <el-form-item label="可见性">
            <el-radio-group v-model="form.visibility">
              <el-radio label="public">公开发布</el-radio>
              <el-radio label="private">私密草稿</el-radio>
            </el-radio-group>
            <span class="form-tip">公开发布后所有人可见，私密草稿仅管理员可查看</span>
          </el-form-item>

          <!-- 置顶文章 -->
          <el-form-item label="置顶文章">
            <el-switch v-model="isTop" />
            <span class="form-tip">置顶文章将显示在列表顶部</span>
          </el-form-item>

          <!-- 操作按钮 -->
          <el-form-item>
            <div class="form-actions">
              <el-button @click="handleCancel">取消</el-button>
              <el-button type="primary" :loading="isSubmitting" @click="handleSubmit">
                {{ isSubmitting ? '提交中...' : (isEditMode ? '保存修改' : '立即发布') }}
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.publish-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.publish-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--warm-950);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.title-icon {
  color: var(--warm-600);
  font-size: 2rem;
}

.page-subtitle {
  color: var(--warm-700);
  font-size: 1.1rem;
}

.publish-content {
  min-height: 600px;
}

.publish-card {
  border-radius: 1rem;
}

.upload-area {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.upload-tip {
  font-size: 0.875rem;
  color: var(--warm-700);
}

.cover-preview {
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.form-tip {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: var(--warm-700);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.form-actions .el-button {
  flex: 1;
  max-width: 200px;
}

.content-editor-header {
  margin-bottom: 0.75rem;
  width: 100%;
}

.content-preview-area {
  width: 100%;
  min-height: 400px;
  padding: 1.5rem;
  border: 1px solid var(--el-border-color);
  border-radius: 0.5rem;
  background: #fff;
  overflow-y: auto;
}
</style>
