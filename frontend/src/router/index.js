import { createRouter, createWebHistory } from "vue-router"

import LoginView from "../views/LoginView.vue"
import RegisterView from "../views/RegisterView.vue"
import AdminDashboard from "../views/AdminDashboard.vue"
import UserDashboard from "../views/UserDashboard.vue"
import StaffDashboard from "../views/StaffDashboard.vue"
import ManageTreks from "../views/ManageTreks.vue"
import ManageStaff from "../views/ManageStaff.vue"
import AdminBookings from "../views/AdminBookings.vue"
import ManageUsers from "../views/ManageUsers.vue"
import MyBookings from "../views/MyBookings.vue"
import Profile from "../views/Profile.vue"
import Participants from "../views/Participants.vue"
import Reports from "../views/Reports.vue"



const routes = [
    {
        path: "/",
        redirect: "/login"
    },
    {
        path: "/login",
        component: LoginView
    },
    {
        path: "/register",
        component: RegisterView
    },

    {
    path: "/admin",
    component: AdminDashboard
    },
    {
    path: "/user",
    component: UserDashboard
},
{
    path: "/staff",
    component: StaffDashboard
},

{
    path: "/admin/treks",
    component: ManageTreks
},
{
    path: "/admin/staff",
    component: ManageStaff
},
{
    path: "/admin/users",
    component: ManageUsers
},

{
    path: "/admin/bookings",
    component: AdminBookings
},
{
    path: "/user/bookings",
    component: MyBookings
},
{
    path: "/profile",
    component: Profile
},
{
    path: "/staff/treks/:id/participants",
    component: Participants
},
{
    path: "/admin/reports",
    component: Reports
}




]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router