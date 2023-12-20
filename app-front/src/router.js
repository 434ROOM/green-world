import { createRouter, createWebHistory } from 'vue-router';
//Pages 文件名要大写
import Test from './pages/Test.vue';
import Home from './pages/Home.vue';

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