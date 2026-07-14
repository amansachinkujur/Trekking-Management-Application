<template>

<div class="container mt-5">

    <h2 class="mb-4">
        My Bookings
    </h2>

    <button
        class="btn btn-primary mb-3"
        @click="loadBookings"
    >
        Refresh Bookings
    </button>

    <button
            class="btn btn-success mb-3 ms-2"
            @click="exportBookings"
        >
            Export Booking History
        </button>

    <table class="table table-bordered table-striped">

        <thead>

            <tr>

                <th>Booking ID</th>
                <th>Trek Name</th>
                <th>Assigned Staff</th>
                <th>Booking Date</th>
                <th>Status</th>
                <th>Payment Status</th>
                <th>Action</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="booking in bookings"
                :key="booking.booking_id"
            >

                <td>{{ booking.booking_id }}</td>

                <td>{{ booking.trek_name }}</td>

                <td>{{ booking.staff_name || "Not Assigned" }}</td>

                <td>{{ booking.booking_date }}</td>

                <td>{{ booking.status }}</td>

                <td>{{ booking.payment_status }}</td>

               

                        <td>

                            <button
                                v-if="booking.status !== 'Cancelled'"
                                class="btn btn-danger btn-sm"
                                @click="cancelBooking(booking.booking_id)"
                            >
                                Cancel Booking
                            </button>

                        </td>
              

            </tr>

        </tbody>

    </table>

</div>

</template>




<script setup>

import { ref, onMounted } from "vue"
import { API_URL } from "../config"

const bookings = ref([])

async function loadBookings() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/bookings`, {

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

async function cancelBooking(bookingId) {

    if (!confirm("Are you sure you want to cancel this booking?")) {

        return

    }

    const token = localStorage.getItem("token")

    const response = await fetch(

        `${API_URL}/bookings/${bookingId}/cancel`,

        {

            method: "PUT",

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    )

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        loadBookings()

    }
    else {

        alert(data.message || data.msg)

    }

}

async function exportBookings() {

    const token = localStorage.getItem("token")

    const response = await fetch(

        `${API_URL}/bookings/export`,

        {

            method: "POST",

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    )

    const data = await response.json()

    alert(data.message)

}



onMounted(() => {

    loadBookings()

})

</script>