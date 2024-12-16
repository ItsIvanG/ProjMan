import {createRouter, createWebHistory} from 'vue-router';
import Dashboard from './pages/Dashboard.vue';
import Login from './pages/Login.vue';
import forgotpass from './pages/forgotpass.vue';
import Register from "./pages/Register.vue";
import RegisterLegacy from "./pages/RegisterLegacy.vue";

import Member from "./pages/Member.vue";
import Report from "./pages/Report.vue";
import Task from "./pages/Project Management/Task.vue";
import OwnTask from "./pages/Project Management/Owntask.vue";
import Gantt from "./pages/Project Management/Gantt.vue";
import Kanban from "./pages/Project Management/Kanban.vue";
import Kanban2 from "./pages/Project Management/Kanban2.vue";
import Profile from "./pages/Profile.vue";

import Sprint from "./pages/Project Management/Sprint.vue";
import Sharing from "./pages/Sharing.vue";
import MemberReport from "./pages/MemberReport.vue";



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
        path: '/own-task',
        name: 'own-task',
        component: OwnTask
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
        path: '/kanban2',
        name: 'kanban2',
        component: Kanban2
    },
    {
        path: '/gantt',
        name: 'gantt',
        component: Gantt
    },
    {
        path: '/sprint',
        name: 'sprint',
        component: Sprint
    },
    {
        path: '/sharing',
        name: 'sharing',
        component: Sharing
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
    },
{
        path: '/registerlegacy',
        name: 'registerlegacy',
        component: RegisterLegacy
    },
    {
        path: '/forgotpass',
        name: 'notification',
        component: forgotpass
    },
        {
        path: '/profile',
        name: 'profile',
        component: Profile
    },
        {
        path: '/memberreport',
        name: 'memberreport',
        component: MemberReport
    }

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router