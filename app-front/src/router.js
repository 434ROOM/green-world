import { createRouter, createWebHistory } from 'vue-router';
//Pages 文件名要大写

const routes = [
  {
    path: '/test',
    name: 'Test',
    component: () => import('./pages/Test.vue') // 路由懒加载
  },
  {
    path:'/',
    name:'Home',
    component: () => import('./pages/Home.vue')
  },
  {
    path:'/index',
    redirect:'/'
  },
  {
    path:'/home',
    redirect:'/'
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('./pages/About.vue')
  },
  {
    path: '/video',
    name: 'Video',
  },
  {
    path: '/audio',
    name: 'Audio',
  },
  {
    path: '/image',
    name: 'Image',
  }
  // 其他路由配置...
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;