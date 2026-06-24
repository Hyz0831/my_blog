import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios'

// --- 类型定义 ---

export interface PostItem {
    id: number
    user_id: number
    title: string
    content: string
    content_type: string
    summary: string
    cover_img: string
    views: number
    tags: string | string[]
    status: number
    visibility: number
    likes: number
    comments_count: number
    created_at: string
    updated_at: string
}

export interface ApiResponse<T = any> {
    code: number
    msg: string
    data: T
    total?: number
    page?: number
    page_size?: number
}

export interface Data_count {
    texts_count: number
    read_count: number
    customer_count: number
}

export interface CategoryItem {
    id: number
    name: string
    slug: string
    count: number
}

export interface TagItem {
    id: number
    name: string
    slug: string
    count: number
}

export interface CommentItem {
    id: number
    post_id: number
    user_id: number
    nickname: string
    avatar: string
    content: string
    parent_id: number | null
    likes: number
    created_at: string
    replies?: CommentItem[]
}

export interface CreateCommentParams {
    post_id: number
    content: string
    nickname: string
    email?: string
    parent_id?: number
}

export interface ResourceItem {
    id: number
    name: string
    role: string
    experience: string
    company: string
    location: string
    skills: string[]
    description: string
    cover_img: string
    file_path: string
    filename: string
    has_password: boolean
}

export interface VerifyResourceParams {
    resource_id: number
    password: string
}

export interface ProfileInfo {
    nickname: string
    avatar: string
    title: string
    subtitle: string
    bio: string
    tech_stack: {
        category: string
        items: string[]
    }[]
    contacts: {
        platform: string
        url: string
        icon: string
    }[]
    features: {
        title: string
        description: string
        icon: string
    }[]
}

// --- Axios 实例配置 ---

const api: AxiosInstance = axios.create({
    /**
     * ✅ 关键修复：
     * 1. 生产环境：使用相对路径 '/api'，请求会发给当前域名 (https://mgj-hyz.icu/api/...)
     *    Nginx 会将其代理到后端容器。
     * 2. 开发环境：建议在 .env.development 中设置 VITE_API_BASE_URL=http://localhost:8000/api
     * 3. 兜底：如果没有环境变量，默认使用 '/api' (适用于部署后)
     */
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})

// --- 请求拦截器 ---

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error: AxiosError) => {
        console.error('请求配置错误:', error)
        return Promise.reject(error)
    }
)

// --- 响应拦截器 ---

api.interceptors.response.use(
    (response: AxiosResponse<ApiResponse>) => {
        const responseData = response.data as ApiResponse

        // 处理业务逻辑错误码
        if (responseData.code === 401) {
            localStorage.removeItem('access_token')
            // 如果是单页应用，建议使用 router.push('/') 而不是直接跳转，避免刷新
            // window.location.href = '/' 
            return Promise.reject(new Error('登录已过期，请重新登录'))
        }

        if (responseData.code !== 200) {
            return Promise.reject(new Error(responseData.msg || '请求失败'))
        }

        return response
    },
    (error: AxiosError) => {
        console.error('HTTP 请求错误:', error)

        // 提取更友好的错误信息
        const errorResponse = error.response?.data as Partial<ApiResponse> | undefined
        const errorMessage = errorResponse?.msg ||
            error.response?.statusText ||
            error.message ||
            '网络请求失败，请检查网络连接或后端服务状态'

        return Promise.reject(new Error(errorMessage))
    }
)

// --- 工具函数：解析数组格式数据 ---

/**
 * 解析后端返回的数组格式帖子数据
 * ⚠️ 请确保字段索引与后端 SQLite 查询结果严格一致
 */
const parsePostArray = (fields: any[]): PostItem => {
    const safeGet = (index: number, defaultValue: any = '') =>
        fields[index] !== undefined ? fields[index] : defaultValue

    return {
        id: Number(safeGet(0)) || 0,
        user_id: Number(safeGet(1)) || 0,
        title: String(safeGet(2)),
        // 注意：根据你的后端 SQL，索引 3 可能是 author_id 或其他，这里跳过
        content: String(safeGet(4)),        
        content_type: String(safeGet(5)),
        summary: String(safeGet(6)),
        cover_img: String(safeGet(7)),
        views: Number(safeGet(8)) || 0,
        tags: safeGet(9), // 保持原样，后续在 computed 中处理
        status: Number(safeGet(10)) || 0,
        visibility: Number(safeGet(11)) || 0,
        // 假设索引 12 是其他字段，跳过
        likes: Number(safeGet(13)) || 0,         
        comments_count: Number(safeGet(14)) || 0,
        // 假设索引 15 是其他字段，跳过
        created_at: String(safeGet(16)),    
        updated_at: String(safeGet(17))
    }
}

// --- API 接口导出 ---

/**
 * 获取文章列表
 */
export const get_texts = async (page: number = 1, size: number = 8): Promise<ApiResponse<PostItem[]>> => {
    console.log('📄 API 调用 - get_texts:', { page, size })
    
    // baseURL='/api' + url='/posts' => 最终请求: /api/posts
    const response = await api.get<ApiResponse<any[]>>('/posts', {
        params: { page, page_size: size } // 注意：后端参数名通常是 page_size 还是 size? 根据你之前的 FastAPI 代码是 page_size
    })

    const result = response.data

    // 如果后端返回的是数组包裹的数据，进行解析
    if (result.data && Array.isArray(result.data)) {
        result.data = result.data.map((item: any) => {
            if (Array.isArray(item)) {
                return parsePostArray(item)
            }
            return item as PostItem
        })
    }

    return result
}

/**
 * 获取文章详情
 */
export const get_text_detail = async (id: string | number): Promise<ApiResponse<PostItem>> => {
    console.log('📄 API 调用 - get_text_detail:', { id })
    
    // baseURL='/api' + url='/posts/${id}' => 最终请求: /api/posts/1
    const response = await api.get<ApiResponse<any>>(`/posts/${id}`)

    const result = response.data

    // 兼容后端可能返回数组或对象的情况
    if (result.data) {
        if (Array.isArray(result.data)) {
            result.data = parsePostArray(result.data)
        } else if (typeof result.data === 'object') {
            // 如果已经是对象，确保类型转换
            result.data = result.data as PostItem
        }
    }

    return result
}

/**
 * 📊 获取全站数据统计
 */
export const get_data_count = async (params?: {
    start_date?: string
    end_date?: string
    user_id?: number
}): Promise<ApiResponse<Data_count>> => {
    console.log('📊 API 调用 - get_data_count:', params)
    
    // baseURL='/api' + url='/data_count' => 最终请求: /api/data_count
    const response = await api.get<ApiResponse<Data_count>>('/data_count', {
        params: params || undefined
    })
    
    return response.data
}

export const get_recent_posts = async (limit: number = 5): Promise<ApiResponse<PostItem[]>> => {
    console.log('📄 API 调用 - get_recent_posts:', { limit })
    const response = await api.get<ApiResponse<PostItem[]>>('/posts/recent', {
        params: { limit }
    })
    return response.data
}

export const get_top_posts = async (limit: number = 5): Promise<ApiResponse<PostItem[]>> => {
    console.log('🔥 API 调用 - get_top_posts:', { limit })
    const response = await api.get<ApiResponse<PostItem[]>>('/posts/top', {
        params: { limit }
    })
    return response.data
}

export const get_categories = async (): Promise<ApiResponse<CategoryItem[]>> => {
    console.log('📁 API 调用 - get_categories')
    const response = await api.get<ApiResponse<CategoryItem[]>>('/categories')
    return response.data
}

export const get_tags = async (): Promise<ApiResponse<TagItem[]>> => {
    console.log('🏷️ API 调用 - get_tags')
    const response = await api.get<ApiResponse<TagItem[]>>('/tags')
    return response.data
}

export const get_posts_by_category = async (
    categorySlug: string,
    page: number = 1,
    size: number = 8
): Promise<ApiResponse<PostItem[]>> => {
    console.log('📁 API 调用 - get_posts_by_category:', { categorySlug, page, size })
    const response = await api.get<ApiResponse<PostItem[]>>(`/categories/${categorySlug}/posts`, {
        params: { page, size }
    })
    return response.data
}

export const get_posts_by_tag = async (
    tagSlug: string,
    page: number = 1,
    size: number = 8
): Promise<ApiResponse<PostItem[]>> => {
    console.log('🏷️ API 调用 - get_posts_by_tag:', { tagSlug, page, size })
    const response = await api.get<ApiResponse<PostItem[]>>(`/tags/${tagSlug}/posts`, {
        params: { page, size }
    })
    return response.data
}

export const get_posts_by_tags = async (
    tagSlugs: string[],
    category?: string,
    page: number = 1,
    size: number = 8
): Promise<ApiResponse<PostItem[]>> => {
    console.log('🏷️🔗 API 调用 - get_posts_by_tags:', { tagSlugs, category, page, size })
    const params: Record<string, any> = { page, size }
    if (tagSlugs.length > 0) params.tags = tagSlugs.join(',')
    if (category && category !== 'all') params.category = category
    const response = await api.get<ApiResponse<PostItem[]>>('/posts/filter', { params })
    return response.data
}

export const search_posts = async (
    keyword: string,
    page: number = 1,
    size: number = 8
): Promise<ApiResponse<PostItem[]>> => {
    console.log('🔍 API 调用 - search_posts:', { keyword, page, size })
    const response = await api.get<ApiResponse<PostItem[]>>('/posts/search', {
        params: { keyword, page, size }
    })
    return response.data
}

export const like_post = async (id: number | string): Promise<ApiResponse<{ likes: number }>> => {
    console.log('❤️ API 调用 - like_post:', { id })
    const response = await api.post<ApiResponse<{ likes: number }>>(`/posts/${id}/like`)
    return response.data
}

export const get_comments = async (
    postId: number | string,
    page: number = 1,
    size: number = 20
): Promise<ApiResponse<CommentItem[]>> => {
    console.log('💬 API 调用 - get_comments:', { postId, page, size })
    const response = await api.get<ApiResponse<CommentItem[]>>(`/posts/${postId}/comments`, {
        params: { page, size }
    })
    return response.data
}

export const create_comment = async (data: CreateCommentParams): Promise<ApiResponse<CommentItem>> => {
    console.log('✍️ API 调用 - create_comment:', data)
    const response = await api.post<ApiResponse<CommentItem>>('/comments', data)
    return response.data
}

export const like_comment = async (commentId: number | string): Promise<ApiResponse<{ likes: number }>> => {
    console.log('❤️ API 调用 - like_comment:', { commentId })
    const response = await api.post<ApiResponse<{ likes: number }>>(`/comments/${commentId}/like`)
    return response.data
}

export const get_resources = async (): Promise<ApiResponse<ResourceItem[]>> => {
    console.log('🔐 API 调用 - get_resources')
    const response = await api.get<ApiResponse<ResourceItem[]>>('/resources')
    return response.data
}

export const verify_resource_password = async (data: VerifyResourceParams): Promise<ApiResponse<{ access_token: string; file_path: string }>> => {
    console.log('🔑 API 调用 - verify_resource_password:', { resource_id: data.resource_id })
    const response = await api.post<ApiResponse<{ access_token: string; file_path: string }>>('/resources/verify', data)
    return response.data
}

// --- 文章发布与管理 ---

export interface PublishPostRequest {
    title: string
    content: string
    content_format?: string
    summary?: string
    cover_img?: string
    tags?: string
    category_id?: number
    visibility?: 'public' | 'private'
    is_top?: number
}

export const publish_post = async (data: PublishPostRequest): Promise<ApiResponse<any>> => {
    console.log('📝 API 调用 - publish_post:', { title: data.title })
    const response = await api.post<ApiResponse<any>>('/posts/publish', data)
    return response.data
}

export const edit_post = async (id: number, data: PublishPostRequest): Promise<ApiResponse<any>> => {
    console.log('📝 API 调用 - edit_post:', { id, title: data.title })
    const response = await api.put<ApiResponse<any>>(`/posts/${id}`, data)
    return response.data
}

export const delete_post = async (id: number): Promise<ApiResponse<any>> => {
    console.log('🗑️ API 调用 - delete_post:', { id })
    const response = await api.delete<ApiResponse<any>>(`/posts/${id}`)
    return response.data
}

// --- 个人资料 ---

export const update_profile = async (data: Partial<ProfileInfo>): Promise<ApiResponse<null>> => {
    console.log('👤 API 调用 - update_profile:', data)
    const response = await api.put<ApiResponse<null>>('/profile', data)
    return response.data
}

export const upload_image = async (file: File): Promise<ApiResponse<{ url: string; filename: string }>> => {
    console.log('📸 API 调用 - upload_image:', file.name)
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post<ApiResponse<{ url: string; filename: string }>>('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
}

// --- 其他 ---

export const get_profile = async (): Promise<ApiResponse<ProfileInfo>> => {
    console.log('👤 API 调用 - get_profile')
    const response = await api.get<ApiResponse<ProfileInfo>>('/profile')
    return response.data
}

export const subscribe_email = async (email: string): Promise<ApiResponse<{ email: string }>> => {
    console.log('📧 API 调用 - subscribe_email:', email)
    const response = await api.post<ApiResponse<{ email: string }>>('/subscribe', { email })
    return response.data
}

export default api