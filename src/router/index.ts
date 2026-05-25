import { createRouter, createWebHistory } from 'vue-router'
import DateSelection from '../components/DateSelection.vue'
import Settings from '../components/Settings.vue'
import MyAppointments from '../components/MyAppointments.vue'
import AuthPage from '../components/AuthPage.vue'
import StaffDashboard from '../components/StaffDashboard.vue'
import Terms from '../components/Terms.vue'
import Privacy from '../components/Privacy.vue'

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
    },
    {
        path: '/terms',
        name: 'Terms',
        component: Terms
    },
    {
        path: '/privacy',
        name: 'Privacy',
        component: Privacy
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
