<template>

<div class="container mt-5">

    <h2 class="mb-4">
        All Bookings
    </h2>

    <button
        class="btn btn-primary mb-3"
        @click="loadBookings"
    >
        Refresh Bookings
    </button>

    <div class="row mb-3">

        <div class="col-md-6">

            <label class="form-label">
                Search
            </label>

            <input
                class="form-control"
                placeholder="Search by user or trek"
                v-model="search"
            >

        </div>

    </div>

    <table class="table table-bordered table-striped">

        <thead>

            <tr>

                <th>ID</th>
                <th>User</th>
                <th>Email</th>
                <th>Trek</th>
                <th>Staff</th>
                <th>Booking Date</th>
                <th>Status</th>
                <th>Payment</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="booking in filteredBookings"
                :key="booking.booking_id"
            >

                <td>{{ booking.booking_id }}</td>

                <td>{{ booking.user_name }}</td>

                <td>{{ booking.user_email }}</td>

                <td>{{ booking.trek_name }}</td>

                <td>

                    {{ booking.staff_name || "Not Assigned" }}

                </td>

                <td>{{ booking.booking_date }}</td>

                <td>{{ booking.status }}</td>

                <td>{{ booking.payment_status }}</td>

            </tr>

        </tbody>

    </table>

</div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue"
import { API_URL } from "../config"

const bookings = ref([])

const search = ref("")

const filteredBookings = computed(() => {

    if (!search.value.trim()) {

        return bookings.value

    }

    const query = search.value.toLowerCase()

    return bookings.value.filter(booking =>

        booking.user_name.toLowerCase().includes(query) ||

        booking.user_email.toLowerCase().includes(query) ||

        booking.trek_name.toLowerCase().includes(query)

    )

})

async function loadBookings() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/admin/bookings`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

    const data = await response.json()

    if (response.ok) {

        bookings.value = data

    }
    else {

        alert(data.message || data.msg)

    }

}

onMounted(() => {

    loadBookings()

})

</script>