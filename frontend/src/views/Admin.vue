<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  Document, TrendCharts, User, Edit, Plus, Search,
  DataAnalysis, Files, Setting,
  Refresh, Star, Delete, Lock, Upload
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  get_data_count, get_texts, get_categories, get_tags,
  search_posts, get_posts_by_category, delete_post,
  get_profile, update_profile, upload_image,
  type PostItem, type Data_count, type CategoryItem, type TagItem, type ProfileInfo
} from '../api/api'
import { changePassword } from '../api/auth'

const router = useRouter()
const route = useRoute()

// 当前激活的模块
const activeModule = ref<'dashboard' | 'posts' | 'categories' | 'tags' | 'settings'>('dashboard')

// 加载状态
const loading = ref(false)

// 统计数据
const stats = reactive({
  texts_count: 0,
  read_count: 0,
  customer_count: 0
})

// 文章列表
const posts = ref<PostItem[]>([])
const postsTotal = ref(0)
const postsPage = ref(1)
const postsPageSize = ref(8)

// 搜索与筛选
const searchKeyword = ref('')
const searchCategory = ref<number | ''>('')

// 文章统计（基于当前列表）
const postStats = reactive({
  totalCount: 0,
  draftCount: 0,
  publicCount: 0
})

// 分类与标签
const categories = ref<CategoryItem[]>([])
const tags = ref<TagItem[]>([])

// 侧边菜单
const menuItems = [
  { key: 'dashboard', name: '仪表盘', icon: DataAnalysis },
  { key: 'posts', name: '文章管理', icon: Edit },
  { key: 'categories', name: '分类管理', icon: Files },
  { key: 'tags', name: '标签管理', icon: Star },
  { key: 'settings', name: '系统设置', icon: Setting }
] as const

// 顶部统计卡片
const statCards = computed(() => [
  { icon: Document, value: stats.texts_count, label: '文章总数', color: '#d97706' },
  { icon: TrendCharts, value: stats.read_count, label: '总阅读量', color: '#059669' },
  { icon: User, value: stats.customer_count, label: '访客数量', color: '#7c3aed' },
  { icon: Edit, value: posts.value.length, label: '当前页文章', color: '#dc2626' }
])

// 加载统计数据
const loadStats = async () => {
  try {
    const result = await get_data_count()
    if (result.code === 200 && result.data) {
      const data = result.data as Data_count
      stats.texts_count = data.texts_count
      stats.read_count = data.read_count
      stats.customer_count = data.customer_count
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载文章列表（支持搜索和分类筛选）
const loadPosts = async () => {
  loading.value = true
  try {
    let result
    if (searchKeyword.value) {
      result = await search_posts(searchKeyword.value, postsPage.value, postsPageSize.value)
    } else if (searchCategory.value !== '') {
      const selectedCat = categories.value.find(c => c.id === searchCategory.value)
      if (selectedCat) {
        result = await get_posts_by_category(selectedCat.slug, postsPage.value, postsPageSize.value)
      } else {
        result = await get_texts(postsPage.value, postsPageSize.value)
      }
    } else {
      result = await get_texts(postsPage.value, postsPageSize.value)
    }

    if (result && result.code === 200) {
      posts.value = result.data || []
      postsTotal.value = result.total || 0
      
      // 更新文章统计
      postStats.totalCount = result.total || 0
      postStats.publicCount = posts.value.filter(p => p.visibility === 1 || (p as any).visibility === 'public').length
      postStats.draftCount = postStats.totalCount - postStats.publicCount
    }
  } catch (error) {
    console.error('加载文章列表失败:', error)
    ElMessage.error('加载文章列表失败')
  } finally {
    loading.value = false
  }
}

// 加载分类和标签
const loadCategoriesAndTags = async () => {
  try {
    const [catResult, tagResult] = await Promise.all([
      get_categories(),
      get_tags()
    ])
    if (catResult.code === 200) categories.value = catResult.data || []
    if (tagResult.code === 200) tags.value = tagResult.data || []
  } catch (error) {
    console.error('加载分类标签失败:', error)
  }
}

// 加载全部数据
const loadAll = async () => {
  await Promise.all([loadStats(), loadPosts(), loadCategoriesAndTags()])
}

// 删除文章
const handleDeletePost = async (post: PostItem) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文章「${post.title}」吗？此操作不可撤销。`,
      '删除确认',
      { confirmButtonText: '确定删除', cancelButtonText: '取消', type: 'warning' }
    )
    const result = await delete_post(post.id)
    if (result.code === 200) {
      ElMessage.success('删除成功')
      await loadPosts()
      await loadStats()
    } else {
      ElMessage.error(result.msg || '删除失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 跳转发布文章
const goPublish = () => router.push('/publish')

// 分页改变
const handlePageChange = (val: number) => {
  postsPage.value = val
  loadPosts()
}

// 格式化数字
const formatNumber = (num: number) => {
  if (num >= 10000) return `${(num / 10000).toFixed(1)}w`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}k`
  return num.toString()
}

onMounted(() => {
  loadAll()
})

// 修改密码
const changePwdLoading = ref(false)
const pwdForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const handleChangePassword = async () => {
  if (!pwdForm.old_password) {
    ElMessage.warning('请输入原密码')
    return
  }
  if (!pwdForm.new_password) {
    ElMessage.warning('请输入新密码')
    return
  }
  if (pwdForm.new_password.length < 6) {
    ElMessage.warning('新密码长度至少6位')
    return
  }
  if (pwdForm.new_password !== pwdForm.confirm_password) {
    ElMessage.warning('两次输入的新密码不一致')
    return
  }

  changePwdLoading.value = true
  try {
    const result = await changePassword({
      old_password: pwdForm.old_password,
      new_password: pwdForm.new_password
    })
    if (result.code === 200) {
      ElMessage.success('密码修改成功，请重新登录')
      localStorage.removeItem('access_token')
      localStorage.removeItem('username')
      router.push('/admin/login')
    } else {
      ElMessage.error(result.msg || '修改失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '修改密码失败')
  } finally {
    changePwdLoading.value = false
  }
}

// 个人资料编辑
const profileLoading = ref(false)
const profileSaving = ref(false)
const profileForm = reactive({
  nickname: '',
  title: '',
  subtitle: '',
  bio: '',
  avatar: ''
})

const loadProfile = async () => {
  profileLoading.value = true
  try {
    const result = await get_profile()
    if (result.code === 200 && result.data) {
      const p = result.data as ProfileInfo
      profileForm.nickname = p.nickname || ''
      profileForm.title = p.title || ''
      profileForm.subtitle = p.subtitle || ''
      profileForm.bio = p.bio || ''
      profileForm.avatar = p.avatar || ''
    }
  } catch (error) {
    console.error('加载个人资料失败:', error)
  } finally {
    profileLoading.value = false
  }
}

const handleSaveProfile = async () => {
  if (!profileForm.nickname.trim()) {
    ElMessage.warning('昵称不能为空')
    return
  }
  profileSaving.value = true
  try {
    const result = await update_profile({
      nickname: profileForm.nickname,
      title: profileForm.title,
      subtitle: profileForm.subtitle,
      bio: profileForm.bio,
      avatar: profileForm.avatar
    })
    if (result.code === 200) {
      ElMessage.success('个人资料更新成功')
    } else {
      ElMessage.error(result.msg || '更新失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '更新个人资料失败')
  } finally {
    profileSaving.value = false
  }
}

// 头像上传
const avatarUploading = ref(false)
const handleAvatarUpload = async (options: any) => {
  const file = options.file as File
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    return
  }

  avatarUploading.value = true
  try {
    const result = await upload_image(file)
    if (result.code === 200 && result.data) {
      profileForm.avatar = result.data.url
      ElMessage.success('头像上传成功，请点击"保存资料"确认')
    } else {
      ElMessage.error(result.msg || '上传失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '头像上传失败')
  } finally {
    avatarUploading.value = false
  }
}

// 监听 refresh 参数，从发布/编辑页返回时自动刷新数据
watch(() => route.query.refresh, (val) => {
  if (val) {
    loadAll()
    router.replace({ path: '/admin' })
  }
})

// 切换到设置模块时加载个人资料
watch(activeModule, (val) => {
  if (val === 'settings') {
    loadProfile()
  }
})
</script>

<template>
  <div class="admin-page">
    <!-- 顶部头部 -->
    <header class="admin-header">
      <div class="header-left">
        <h1 class="page-title">
          <el-icon class="title-icon"><Setting /></el-icon>
          管理后台
        </h1>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="goPublish">
          发布文章
        </el-button>
        <el-button :icon="Refresh" @click="loadAll" circle />
      </div>
    </header>

    <div class="admin-body">
      <!-- 侧边菜单 -->
      <aside class="admin-sidebar">
        <nav class="sidebar-nav">
          <button
            v-for="item in menuItems"
            :key="item.key"
            class="nav-btn"
            :class="{ active: activeModule === item.key }"
            @click="activeModule = item.key"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.name }}</span>
          </button>
        </nav>
      </aside>

      <!-- 主内容区 -->
      <main class="admin-main">
        <!-- 仪表盘 -->
        <section v-if="activeModule === 'dashboard'" class="module-content">
          <!-- 统计卡片 -->
          <div class="stat-cards">
            <div v-for="(card, index) in statCards" :key="index" class="stat-card" :style="{ borderLeftColor: card.color }">
              <div class="stat-icon" :style="{ color: card.color, background: card.color + '15' }">
                <el-icon :size="24"><component :is="card.icon" /></el-icon>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ formatNumber(Number(card.value)) }}</span>
                <span class="stat-label">{{ card.label }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 文章管理 -->
        <section v-else-if="activeModule === 'posts'" class="module-content">
          <el-card class="content-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><Edit /></el-icon>
                  文章管理 (共 {{ postsTotal }} 篇)
                </span>
                <div class="header-actions">
                  <el-input
                    v-model="searchKeyword"
                    placeholder="搜索文章..."
                    :prefix-icon="Search"
                    clearable
                    style="width: 250px"
                    @clear="loadPosts"
                    @keyup.enter="loadPosts"
                  />
                  <el-select v-model="searchCategory" placeholder="按分类筛选" clearable @change="loadPosts" style="width: 180px">
                    <el-option
                      v-for="cat in categories"
                      :key="cat.id"
                      :label="cat.name"
                      :value="cat.id"
                    />
                  </el-select>
                  <el-button type="primary" :icon="Plus" @click="goPublish">发布新文章</el-button>
                </div>
              </div>
            </template>
            
            <el-table :data="posts" v-loading="loading" border style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" min-width="250" show-overflow-tooltip />
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="(row.visibility === 1 || row.visibility === 'public') ? 'success' : 'info'" size="small">
                    {{ (row.visibility === 1 || row.visibility === 'public') ? '公开' : '私密' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="views" label="阅读" width="80" />
              <el-table-column prop="created_at" label="发布时间" width="180">
                <template #default="{ row }">
                  {{ new Date(row.created_at).toLocaleString() }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" type="primary" :icon="Edit" @click="router.push(`/publish/${row.id}`)">编辑</el-button>
                  <el-button size="small" type="danger" :icon="Delete" @click="handleDeletePost(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="pagination-container" v-if="postsTotal > postsPageSize">
              <el-pagination
                background
                layout="prev, pager, next"
                :total="postsTotal"
                :page-size="postsPageSize"
                :current-page="postsPage"
                @current-change="handlePageChange"
              />
            </div>
          </el-card>
        </section>

        <!-- 分类管理 -->
        <section v-else-if="activeModule === 'categories'" class="module-content">
          <el-card class="content-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><Files /></el-icon>
                  分类管理 (共 {{ categories.length }} 个)
                </span>
                <el-button type="primary" :icon="Plus" @click="ElMessage.info('分类创建功能开发中')">新建分类</el-button>
              </div>
            </template>
            <el-table :data="categories" border style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="分类名称" min-width="200" />
              <el-table-column prop="slug" label="Slug" min-width="200" />
              <el-table-column prop="count" label="文章数" width="100">
                <template #default="{ row }">
                  <el-tag type="info">{{ row.count }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default>
                  <el-button size="small" type="primary" :icon="Edit" @click="ElMessage.info('编辑功能开发中')">编辑</el-button>
                  <el-button size="small" type="danger" :icon="Delete" @click="ElMessage.info('删除功能开发中')">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </section>

        <!-- 标签管理 -->
        <section v-else-if="activeModule === 'tags'" class="module-content">
          <el-card class="content-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><Star /></el-icon>
                  标签管理 (共 {{ tags.length }} 个)
                </span>
                <el-button type="primary" :icon="Plus" @click="ElMessage.info('标签创建功能开发中')">新建标签</el-button>
              </div>
            </template>
            <el-table :data="tags" border style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="标签名称" min-width="200" />
              <el-table-column prop="slug" label="Slug" min-width="200" />
              <el-table-column prop="count" label="文章数" width="100">
                <template #default="{ row }">
                  <el-tag type="info">{{ row.count }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default>
                  <el-button size="small" type="primary" :icon="Edit" @click="ElMessage.info('编辑功能开发中')">编辑</el-button>
                  <el-button size="small" type="danger" :icon="Delete" @click="ElMessage.info('删除功能开发中')">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </section>

        <!-- 系统设置模块 -->
        <section v-else-if="activeModule === 'settings'" class="module-content">
          <!-- 个人资料 -->
          <el-card class="content-card" v-loading="profileLoading">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><User /></el-icon>
                  个人资料
                </span>
              </div>
            </template>
            <el-form label-width="100px" class="settings-form">
              <el-form-item label="头像">
                <div class="avatar-upload-section">
                  <el-upload
                    :show-file-list="false"
                    :before-upload="() => false"
                    :http-request="handleAvatarUpload"
                    accept="image/jpeg,image/png,image/gif,image/webp"
                    class="avatar-uploader"
                  >
                    <div class="avatar-upload-trigger">
                      <img v-if="profileForm.avatar" :src="profileForm.avatar" class="avatar-upload-img" />
                      <div v-else class="avatar-upload-placeholder">
                        <el-icon :size="24"><Upload /></el-icon>
                        <span>上传头像</span>
                      </div>
                      <div class="avatar-upload-overlay" v-if="avatarUploading">
                        <span>上传中...</span>
                      </div>
                    </div>
                  </el-upload>
                  <div class="avatar-upload-tips">
                    <p>支持 JPG、PNG、GIF 格式，最大 5MB</p>
                    <el-input
                      v-model="profileForm.avatar"
                      placeholder="或直接输入图片 URL"
                      size="small"
                      style="max-width: 400px; margin-top: 0.5rem"
                    />
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="昵称">
                <el-input
                  v-model="profileForm.nickname"
                  placeholder="请输入昵称"
                  maxlength="20"
                  show-word-limit
                  style="max-width: 300px"
                />
              </el-form-item>
              <el-form-item label="头衔">
                <el-input
                  v-model="profileForm.title"
                  placeholder="例如：全栈开发者"
                  maxlength="30"
                  style="max-width: 300px"
                />
              </el-form-item>
              <el-form-item label="副标题">
                <el-input
                  v-model="profileForm.subtitle"
                  placeholder="例如：热爱技术，分享知识"
                  maxlength="50"
                  style="max-width: 400px"
                />
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input
                  v-model="profileForm.bio"
                  type="textarea"
                  :rows="3"
                  placeholder="一段话介绍自己"
                  maxlength="200"
                  show-word-limit
                  style="max-width: 500px"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="profileSaving" @click="handleSaveProfile">
                  保存资料
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 系统设置 -->
          <el-card class="content-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </span>
              </div>
            </template>
            <el-form label-width="120px" class="settings-form">
              <el-form-item label="站点标题">
                <el-input model-value="Kang的博客" placeholder="请输入站点标题" />
              </el-form-item>
              <el-form-item label="站点描述">
                <el-input type="textarea" :rows="3" placeholder="请输入站点描述" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="ElMessage.info('保存功能开发中')">保存设置</el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 修改密码 -->
          <el-card class="content-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><Lock /></el-icon>
                  修改密码
                </span>
              </div>
            </template>
            <el-form label-width="100px" class="settings-form" @submit.prevent="handleChangePassword">
              <el-form-item label="原密码">
                <el-input
                  v-model="pwdForm.old_password"
                  type="password"
                  placeholder="请输入当前密码"
                  show-password
                  style="max-width: 400px"
                />
              </el-form-item>
              <el-form-item label="新密码">
                <el-input
                  v-model="pwdForm.new_password"
                  type="password"
                  placeholder="请输入新密码（至少6位）"
                  show-password
                  style="max-width: 400px"
                />
              </el-form-item>
              <el-form-item label="确认新密码">
                <el-input
                  v-model="pwdForm.confirm_password"
                  type="password"
                  placeholder="请再次输入新密码"
                  show-password
                  style="max-width: 400px"
                  @keyup.enter="handleChangePassword"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="changePwdLoading" @click="handleChangePassword">
                  修改密码
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  min-height: 100vh;
  padding: 90px 2rem 2rem;
  max-width: 1500px;
  margin: 0 auto;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid var(--warm-200, #fde68a);
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--warm-950, #433422);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-right {
  display: flex;
  gap: 1rem;
}

.admin-body {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 2rem;
}

.admin-sidebar {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border: none;
  background: transparent;
  border-radius: 0.75rem;
  cursor: pointer;
  font-size: 0.95rem;
  color: var(--warm-700, #574a3a);
  transition: all 0.2s;
}

.nav-btn:hover {
  background: var(--warm-50, #fdf8f0);
  color: var(--warm-900, #2e2318);
}

.nav-btn.active {
  background: var(--warm-900, #2e2318);
  color: white;
  font-weight: 600;
}

.admin-main {
  min-height: 600px;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border-left: 4px solid;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--warm-950, #433422);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--warm-700, #574a3a);
  margin-top: 0.25rem;
}

.content-card {
  border-radius: 1rem;
  margin-bottom: 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--warm-950, #433422);
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.pagination-container {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

.module-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.settings-form {
  max-width: 600px;
  padding: 1rem 0;
}

.avatar-upload-section {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}

.avatar-upload-trigger {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px dashed #d9d9d9;
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.3s;
}

.avatar-upload-trigger:hover {
  border-color: var(--warm-500, #d97706);
}

.avatar-upload-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  color: #999;
  font-size: 0.75rem;
}

.avatar-upload-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  border-radius: 50%;
}

.avatar-upload-tips {
  color: #999;
  font-size: 0.8rem;
}

@media (max-width: 1024px) {
  .admin-body {
    grid-template-columns: 1fr;
  }
  
  .admin-sidebar {
    position: static;
  }
  
  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
  }
  
  .stat-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stat-cards {
    grid-template-columns: 1fr;
  }
  
  .header-actions {
    flex-direction: column;
  }
}
</style>
