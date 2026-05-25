import { createRouter, createWebHistory } from 'vue-router'
import DateSelection from '../components/DateSelection.vue'
import Settings from '../components/Settings.vue'
import MyAppointments from '../components/MyAppointments.vue'
import AuthPage from '../components/AuthPage.vue'
import StaffDashboard from '../components/StaffDashboard.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: DateSelection
    },
    {
        path: '/my-appointments',
        name: 'MyAppointments',
        component: MyAppointments
    },
    {
        path: '/admin',
        name: 'Admin',
        component: Settings
    },
    {
        path: '/auth',
        name: 'Auth',
        component: AuthPage
    },
    {
        path: '/staff',
        name: 'Staff',
        component: StaffDashboard
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
