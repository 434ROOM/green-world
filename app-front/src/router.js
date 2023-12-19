import { createRouter, createWebHistory } from 'vue-router';
import Test from './pages/test.vue';
import Home from './pages/home.vue';

const routes = [
  {
    path: '/test',
    name: 'Test',
    component: Test // 定义路由和组件的映射关系
  },
  {
    path:'/',
    name:'Home',
    component: Home
  },
  {
    path:'/index',
    redirect:'/'
  },
  {
    path:'/home',
    redirect:'/'
  }
  // 其他路由配置...
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;