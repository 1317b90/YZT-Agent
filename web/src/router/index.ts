import { createRouter, createWebHistory } from 'vue-router'
import taskView from '../views/task/task.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/task',
      children: [
        {
          path: '/',
          name: 'task-index',
          component: taskView
        },
        {
          path: 'redis',
          name: 'task-redis',
          component: () => import('../views/task/redis.vue')
        },
      ]
    },

    {
      path: "/operation/:operationType",
      name: 'operation',
      component: () => import('../views/operation/index.vue')
    },
    {
      path: "/user",
      name: 'user',
      component: () => import('../views/user/index.vue')
    },
    {
      path: "/message",
      name: 'message',
      component: () => import('../views/message/index.vue')
    },
    {
      path: "/log",
      name: 'log',
      component: () => import('../views/log/index.vue')
    },
  ]
})

export default router
