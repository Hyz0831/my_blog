// src/types/v-md-editor.d.ts

declare module '@kangc/v-md-editor/lib/preview' {
    const component: any;
    export default component;
}

declare module '@kangc/v-md-editor/lib/theme/github.js' {
    const theme: any;
    export default theme;
}

// 如果你以后还用到了插件（如 line-number），也可以在这里继续添加声明
declare module '@kangc/v-md-editor' {
    const component: any;
    export default component;
}