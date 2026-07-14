<template>

<div class="container mt-5">

    <h2 class="mb-4">
        Admin Dashboard
    </h2>

    <div class="row mb-4">

        <div class="col-md-3 mb-3">

            <div class="card text-center">

                <div class="card-body">

                    <h5>Total Treks</h5>

                    <h2>{{ stats.total_treks }}</h2>

                </div>

            </div>

        </div>

        <div class="col-md-3 mb-3">

            <div class="card text-center">

                <div class="card-body">

                    <h5>Total Users</h5>

                    <h2>{{ stats.total_users }}</h2>

                </div>

            </div>

        </div>

        <div class="col-md-3 mb-3">

            <div class="card text-center">

                <div class="card-body">

                    <h5>Total Staff</h5>

                    <h2>{{ stats.total_staff }}</h2>

                </div>

            </div>

        </div>

        <div class="col-md-3 mb-3">

            <div class="card text-center">

                <div class="card-body">

                    <h5>Total Bookings</h5>

                    <h2>{{ stats.total_bookings }}</h2>

                </div>

            </div>

        </div>

    </div>

    <div class="d-grid gap-3">

        <button
            class="btn btn-primary"
            @click="router.push('/admin/treks')"
        >
            Manage Treks
        </button>

        <button
            class="btn btn-success"
            @click="router.push('/admin/staff')"
        >
            Manage Staff
        </button>

        <button
            class="btn btn-success"
            @click="router.push('/admin/users')"
        >
            Manage Users
        </button>

        <button
            class="btn btn-warning"
            @click="router.push('/admin/bookings')"
        >
            View Bookings
        </button>

        <button
            class="btn btn-info"
            @click="router.push('/admin/reports')"
        >
            Reports & Statistics
        </button>

        <button
            class="btn btn-danger"
            @click="logout"
        >
            Logout
        </button>

    </div>

</div>

</template>
<script setup>

import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { API_URL } from "../config"

const router = useRouter()

const stats = ref({

    total_treks: 0,
    total_users: 0,
    total_staff: 0,
    total_bookings: 0

})

async function loadStatistics() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/admin/statistics`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

    const data = await response.json()

    if (response.ok) {

        stats.value = data

    }
    else {

        alert(data.message)

    }

}

function logout() {

    localStorage.clear()

    router.push("/login")

}

onMounted(() => {

    loadStatistics()

})

</script>