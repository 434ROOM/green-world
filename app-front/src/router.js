import { createRouter, createWebHistory } from 'vue-router';
//Pages 文件名要大写

const routes = [
  {
    path: '/test',
    name: 'Test',
    meta: {
      title: '测试'
    },
    component: () => import('./pages/Test.vue') // 路由懒加载
  },
  {
    path: '/',
    name: 'Home',
    meta: {
      title: '首页'
    },
    component: () => import('./pages/Home.vue')
  },
  {
    path: '/index',
    redirect: '/',
  },
  {
    path: '/home',
    redirect: '/',
  },
  {
    path: '/about',
    name: 'About',
    meta: {
      title: '关于我们'
    },
    component: () => import('./pages/About.vue')
  },
  {
    path: '/video',
    name: 'Video',
    meta: {
      title: '视频交互'
    },
    component: () => import('./pages/Video.vue')
  },
  {
    path: '/video/lib',
    name: 'VideoLib',
    meta: {
      title: '视频库'
    },
    component: () => import('./pages/VideoLib.vue')
  },
  {
    path: '/audio',
    name: 'Audio',
    meta: {
      title: '音频交互'
    },
    component: () => import('./pages/Audio.vue')
  },
  {
    path: '/audio/lib',
    name: 'AudioLib',
    meta: {
      title: '音频库'
    },
    component: () => import('./pages/AudioLib.vue')
  },
  {
    path: '/image',
    name: 'Image',
    meta: {
      title: '图像交互'
    },
    component: () => import('./pages/Image.vue')
  },
  {
    path: '/image/lib',
    name: 'ImageLib',
    meta: {
      title: '图像库'
    },
    component: () => import('./pages/ImageLib.vue')
  },
  {
    path:'/:catchAll(.*)',
    name: '404',
    meta: {
      title: '404 Not Found'
    },
    component: () => import('./pages/404.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }; // 滚动到页面顶部
  }
});

// 路由守卫
router.beforeEach((to, from) => {
  // 设置页面标题
  let wholeTitle = to.meta.title + " | GreenWorld - 人与自然和谐共生";
  document.title = wholeTitle;
  return true;
});

export default router;