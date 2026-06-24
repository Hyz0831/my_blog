<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { login } from '../api/auth'

const router = useRouter()
const loading = ref(false)
const loginForm = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    const result = await login(loginForm.value)
    if (result.code === 200 && result.data) {
      localStorage.setItem('access_token', result.data.access_token)
      localStorage.setItem('username', result.data.username)
      ElMessage.success(`欢迎回来, ${result.data.nickname || result.data.username}!`)
      router.push('/admin')
    } else {
      ElMessage.error(result.msg || '登录失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '登录失败，请检查网络')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>管理后台登录</h2>
        <p>请使用管理员账号登录</p>
      </div>
      <el-form :model="loginForm" class="login-form" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input 
            v-model="loginForm.username" 
            placeholder="用户名" 
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="密码" 
            :prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button 
          type="primary" 
          class="login-btn" 
          :loading="loading" 
          @click="handleLogin"
          size="large"
        >
          {{ loading ? '登录中...' : '登录' }}
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fdfbf7 0%, #f5f0e6 100%);
}
.login-card {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.05);
}
.login-header {
  text-align: center;
  margin-bottom: 30px;
}
.login-header h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
}
.login-header p {
  color: #999;
}
.login-btn {
  width: 100%;
  margin-top: 10px;
}
</style>
