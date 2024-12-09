import {createRouter, createWebHistory} from 'vue-router'
import Dashboard from './pages/Dashboard.vue'
import Login from './pages/Login.vue'
import Register from "./pages/Register.vue";
import Member from "./pages/Member.vue";
import Report from "./pages/Report.vue";
import Task from "./pages/Project Management/Task.vue";
import Gantt from "./pages/Project Management/Gantt.vue";
import Kanban from "./pages/Project Management/Kanban.vue";

const routes = [
    {
        path: '/',
        name: 'dashboard',
        component: Dashboard
    },
    {
        path: '/task',
        name: 'task',
        component: Task
    },
    {
        path: '/report',
        name: 'report',
        component: Report
    },
    {
        path: '/member',
        name: 'member',
        component: Member
    },
    {
        path: '/kanban',
        name: 'kanban',
        component: Kanban
    },
    {
        path: '/gantt',
        name: 'gantt',
        component: Gantt
    },
    {
        path: '/login',
        name: 'login',
        component: Login
    },
    {
        path: '/register',
        name: 'register',
        component: Register
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
