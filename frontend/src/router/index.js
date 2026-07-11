import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

import AdminDashboard from '../views/AdminDashboard.vue'
import StaffDashboard from '../views/StaffDashboard.vue'
import TrekkerDashboard from '../views/TrekkerDashboard.vue'

import TreksView from '../views/TreksView.vue'

const routes = [

    {
        path: '/',
        redirect: '/login'
    },

    {
        path: '/login',
        component: LoginView
    },

    {
        path: '/register',
        component: RegisterView
    },

    {
        path: '/admin-dashboard',
        component: AdminDashboard,
        meta: {
            requiresAuth: true,
            role: 'admin'
        }
    },

    {
        path: '/staff-dashboard',
        component: StaffDashboard,
        meta: {
            requiresAuth: true,
            role: 'staff'
        }
    },

    {
        path: '/trekker-dashboard',
        component: TrekkerDashboard,
        meta: {
            requiresAuth: true,
            role: 'trekker'
        }
    },

    {
        path: '/treks',
        component: TreksView,
        meta: {
            requiresAuth: true
        }
    }

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {

    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role')

    if (to.meta.requiresAuth && !token) {
        next({
            path: '/login',
            replace: true
        })
        return
    }

    if (
        to.meta.role &&
        to.meta.role !== role
    ) {
        next({
            path: '/login',
            replace: true
        })
        return
    }

    next()

})

export default router