<template>

<!-- Reports page content -->
<div class="container mt-5">

    <h2 class="mb-4">
        Reports & Trekking Statistics
    </h2>

    <!-- Page actions -->
    <button
        class="btn btn-primary mb-4"
        @click="loadStatistics"
    >
        Refresh
    </button>

    <button
        class="btn btn-secondary mb-4 ms-2"
        @click="router.back()"
    >
        Back
    </button>

    <!-- Statistics table -->
    <table class="table table-bordered table-striped">

        <tbody>

            <tr>
                <th>Total Treks</th>
                <td>{{ stats.total_treks }}</td>
            </tr>

            <tr>
                <th>Total Users</th>
                <td>{{ stats.total_users }}</td>
            </tr>

            <tr>
                <th>Total Staff</th>
                <td>{{ stats.total_staff }}</td>
            </tr>

            <tr>
                <th>Total Bookings</th>
                <td>{{ stats.total_bookings }}</td>
            </tr>

            <tr>
                <th>Open Treks</th>
                <td>{{ stats.open_treks }}</td>
            </tr>

            <tr>
                <th>Completed Treks</th>
                <td>{{ stats.completed_treks }}</td>
            </tr>

            <tr>
                <th>Cancelled Bookings</th>
                <td>{{ stats.cancelled_bookings }}</td>
            </tr>

            <tr>
                <th>Most Popular Trek</th>
                <td>{{ stats.popular_trek }}</td>
            </tr>

        </tbody>

    </table>

</div>

</template>

<script setup>

// Vue imports and API config
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { API_URL } from "../config"

// Router and statistics state
const router = useRouter()

const stats = ref({

    total_treks: 0,
    total_users: 0,
    total_staff: 0,
    total_bookings: 0,
    open_treks: 0,
    completed_treks: 0,
    cancelled_bookings: 0,
    popular_trek: ""

})

// Load statistics from API
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

// Load statistics on page mount
onMounted(() => {

    loadStatistics()

})

</script>