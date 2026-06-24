import axios, { type AxiosInstance } from 'axios'

export interface LoginRequest {
  username: string
  password: string
}

export interface ChangePasswordRequest {
  old_password: string
  new_password: string
}

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器：自动携带 token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 用户登录
export const login = async (data: LoginRequest): Promise<any> => {
  const response = await api.post('/auth/login', data)
  return response.data
}

// 修改密码
export const changePassword = async (data: ChangePasswordRequest): Promise<any> => {
  const response = await api.post('/auth/change-password', data)
  return response.data
}

export default api
