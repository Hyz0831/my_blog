import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import HomeView from '../views/Home.vue'
import FirstView from '../views/First_view.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'firstView',
    component: FirstView,
    meta: { title: '欢迎' }
  },
  {
    path: '/home',
    name: 'Home',
    component: HomeView,
    meta: { title: '主页' }
  },
  {
    path: '/posts',
    name: 'Posts',
    component: () => import('../views/Texts.vue'),
    meta: { title: '文章列表' }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
    meta: { title: '关于我' }
  },
  {
    path: '/resources',
    name: 'Resources',
    component: () => import('../views/Resources.vue'),
    meta: { title: '资源仓库' }
  },
  {
    path: '/posts/:id',
    name: 'PostDetail',
    component: () => import('../views/PostDetail.vue'),
    props: true,
    meta: { title: '文章详情' }
  },
  {
    path: '/resources/detail',
    name: 'ResourceDetail',
    component: () => import('../views/ResourceDetail.vue'),
    meta: { title: '资源详情' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '404 - 页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
  routes
})

router.beforeEach((to, _from, next) => {
  const title = to.meta.title as string || 'MyBlog'
  document.title = `${title} - MyBlog`
  next()
})

export default router