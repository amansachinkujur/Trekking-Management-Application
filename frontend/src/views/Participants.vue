<template>

<!-- Trek participants page -->
<div class="container mt-5">

    <h2 class="mb-4">
        Trek Participants
    </h2>

    <!-- Refresh participants list -->

    <button
        class="btn btn-primary mb-3"
        @click="loadParticipants"
    >
        Refresh
    </button>

    <!-- Go back to previous page -->

    <button
        class="btn btn-secondary mb-3 ms-2"
        @click="router.back()"
    >
        Back
    </button>

    <!-- Participants table -->

    <table class="table table-bordered table-striped">

        <thead>

            <tr>

                <th>Booking ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Booking Date</th>
                <th>Status</th>
                <th>Payment Status</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="booking in participants"
                :key="booking.booking_id"
            >

                <td>{{ booking.booking_id }}</td>

                <td>{{ booking.user_name }}</td>

                <td>{{ booking.user_email }}</td>

                <td>{{ booking.user_phone }}</td>

                <td>{{ booking.booking_date }}</td>

                <td>{{ booking.status }}</td>

                <td>{{ booking.payment_status }}</td>

            </tr>

        </tbody>

    </table>

</div>

</template>



<script setup>

// Vue imports, router, and API config
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { API_URL } from "../config"

// Current route and router
const route = useRoute()

const router = useRouter()

// Participants data
const participants = ref([])

// Load participants from API
async function loadParticipants() {

    const token = localStorage.getItem("token")

    const response = await fetch(

        `${API_URL}/staff/treks/${route.params.id}/bookings`,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    )

    const data = await response.json()

    if (response.ok) {

        participants.value = data

    }
    else {

        alert(data.message)

    }

}

// Load participants on page start
onMounted(() => {

    loadParticipants()

})

</script>