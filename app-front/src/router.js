import { createRouter, createWebHistory } from 'vue-router';
import { message } from 'ant-design-vue';
import JWTToken from './JWTToken.js';
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
      title: '首页',
      requireAuth: false,
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
      title: '关于我们',
      requireAuth: false,
    },
    component: () => import('./pages/About.vue')
  },
  {
    path: '/video',
    name: 'Video',
    meta: {
      title: '视频交互',
      requireAuth: true,
    },
    component: () => import('./pages/Video.vue')
  },
  {
    path: '/video/lib',
    name: 'VideoLib',
    meta: {
      title: '视频库',
      requireAuth: true,
    },
    component: () => import('./pages/VideoLib.vue')
  },
  {
    path: '/audio',
    name: 'Audio',
    meta: {
      title: '音频交互',
      requireAuth: true,
    },
    component: () => import('./pages/Audio.vue')
  },
  {
    path: '/audio/lib',
    name: 'AudioLib',
    meta: {
      title: '音频库',
      requireAuth: true,
    },
    component: () => import('./pages/AudioLib.vue')
  },
  {
    path: '/image',
    name: 'Image',
    meta: {
      title: '图像交互',
      requireAuth: true,
    },
    component: () => import('./pages/Image.vue')
  },
  {
    path: '/image/lib',
    name: 'ImageLib',
    meta: {
      title: '图像库',
      requireAuth: true,
    },
    component: () => import('./pages/ImageLib.vue')
  },
  {
    path: '/login',
    name: 'Login',
    meta: {
      title: '登录',
      requireAuth: false,
    },
    component: () => import('./pages/Login.vue')
  },
  {
    path: '/user',
    name: 'User',
    meta: {
      title: '用户中心',
      requireAuth: true,
    },
    component: () => import('./pages/User.vue')
  },
  {
    path: '/:catchAll(.*)',
    name: '404',
    meta: {
      title: '404 Not Found',
      requireAuth: false,
    },
    component: () => import('./pages/404.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      // 用户通过浏览器的“后退”按钮导航，回到之前保存的滚动位置
      return savedPosition;
    } else {
      // 用户通过页面上的链接跳转，滚动到页面顶部
      return { top: 0 };
    }
  }
});

// 路由守卫
router.beforeEach((to, from) => {
  // 设置页面标题
  let wholeTitle = to.meta.title + " | GreenWorld - 人与自然和谐共生";
  document.title = wholeTitle;
  // 判断该路由是否需要登录权限
  if (to.meta.requireAuth) {
    if (JWTToken.hasToken()) {
      if (JWTToken.isVaildRefreshToken()) {
        if (!JWTToken.isVaildAccessToken()) {
          JWTToken.refreshToken();
        }
        return true;
      } else {
        message.error('登录过期，请重新登录');
      }
    } else {
      message.info('访问此页面需要登录');
    }
    router.replace({
      path: '/login',
      query: { redirect: to.fullPath }
    });
  }
  // 如果已登录，访问登录页面则跳转到首页
  if (to.path === '/login' && JWTToken.hasToken() && JWTToken.isVaildRefreshToken()) {
    message.success('您已登录，无需重复登录');
    router.replace({
      path: '/',
    });
  }
  return true;
});

export default router;