import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// --- 1. Element Plus 核心组件与样式 ---
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 导入 Element Plus 所有图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// --- 2. Markdown 渲染器配置 (v-md-editor @next 版) ---
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';

// 选用 GitHub 主题 (最适合技术文档风格)
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

// --- 3. Prism.js 代码高亮配置 ---
// 基础库
import prism from 'prismjs';
// 常用语言高亮支持 (按需扩展)
import 'prismjs/components/prism-json';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-sql';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-typescript';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-css';
// 导入 Prism 代码高亮的主题样式 (如果主题里没包含)
import 'prismjs/themes/prism.css';

// --- 4. 插件初始化 ---
// 配置 Markdown 预览组件使用 GitHub 主题和 Prism 高亮
VMdPreview.use(githubTheme, {
    Prism: prism,
});

const app = createApp(App)

// --- 5. 全局注册 ---

// 注册 Element Plus 框架
app.use(ElementPlus)

// 注册 Markdown 预览组件 (在模板中使用 <v-md-preview />)
app.use(VMdPreview)

// 全局注册 Element Plus 所有图标，方便直接使用 <CircleClose /> 等标签
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

// 注册路由
app.use(router)

// --- 6. 挂载应用 ---
app.mount('#app')