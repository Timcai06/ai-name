import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/balance',
      name: 'balance',
      component: () => import('../views/BalanceView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('../views/FavoritesView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

// 路由守卫：未登录 → 跳转登录页，非管理员 → 跳转主页
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('ai_naming_token')
  const role = localStorage.getItem('ai_naming_role')
  const requiresAuth = to.meta.requiresAuth

  if (requiresAuth && !token) {
    next('/login')
    return
  }

  // /admin 仅管理员可访问
  if (to.path === '/admin' && role !== 'admin') {
    next('/')
    return
  }

  next()
})

export default router
