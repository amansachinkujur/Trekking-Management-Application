<template>

<div class="container mt-5">

    <h2 class="mb-4">
        Available Treks
    </h2>

    <button
        class="btn btn-primary mb-3"
        @click="loadTreks"
    >
        Refresh Treks
    </button>

        <button
            class="btn btn-warning mb-3 px-3"
            @click="router.push('/user/bookings')"
        >
            My Bookings
        </button>

    <button
        class="btn btn-danger mb-3"
        @click="logout">
        Logout
    </button>
    <button
    class="btn btn-secondary mb-3 ms-2"
    @click="router.push('/profile')"
>
    My Profile
</button>
    <div class="row mb-4">

        <div class="col-md-6">

            <label class="form-label">
                Search Trek
            </label>

            <input
                type="text"
                class="form-control"
                placeholder="Search by trek name"
                v-model="search"
            >

        </div>
<!-- Difficulty -->

<div class="col-md-2">

    <label class="form-label">
        Difficulty
    </label>

    <select
        class="form-select"
        v-model="difficultyFilter"
    >

        <option value="">
            All
        </option>

        <option value="Easy">
            Easy
        </option>

        <option value="Moderate">
            Moderate
        </option>

        <option value="Hard">
            Hard
        </option>

    </select>

</div>

<!-- Duration -->

<div class="col-md-2">

    <label class="form-label">
        Duration
    </label>

    <input
        type="number"
        class="form-control"
        placeholder="Days"
        v-model="durationFilter"
    >

</div>

<!-- Location -->

<div class="col-md-2">

    <label class="form-label">
        Location
    </label>

    <input
        type="text"
        class="form-control"
        placeholder="Location"
        v-model="locationFilter"
    >

</div>


    </div>

    <table class="table table-bordered table-striped">

        <thead>

            <tr>

                <th>Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Duration</th>
                <th>Available Slots</th>
                <th>Assigned Staff</th>
                <th>Status</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Description</th>
                <th>Action</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="trek in filteredTreks"
                :key="trek.id"
            >

                <td>{{ trek.name }}</td>

                <td>{{ trek.location }}</td>

                <td>{{ trek.difficulty }}</td>

                <td>{{ trek.duration }} days</td>

                <td>{{ trek.available_slots }}</td>

                <td>{{ trek.staff_name || "Not Assigned" }}</td>

                <td>{{ trek.status }}</td>

                <td>{{ trek.start_date }}</td>

                <td>{{ trek.end_date }}</td>

                <td>{{ trek.description }}</td>

                <td>

                <button
                    class="btn btn-success btn-sm"
                    @click="bookTrek(trek.id)"
                >
                    Book Trek
                </button>

                </td>

            </tr>

        </tbody>

    </table>

</div>

</template>



<script setup>

import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import { API_URL } from "../config"

const router = useRouter()

const treks = ref([])

const search = ref("")
const difficultyFilter = ref("")

const durationFilter = ref("")

const locationFilter = ref("")


const filteredTreks = computed(() => {

    return treks.value.filter(trek => {

        const matchesSearch =

            trek.name.toLowerCase().includes(search.value.toLowerCase())

        const matchesDifficulty =

            !difficultyFilter.value ||

            trek.difficulty === difficultyFilter.value

        const matchesLocation =

            !locationFilter.value ||

            trek.location
                .toLowerCase()
                .includes(locationFilter.value.toLowerCase())

        const matchesDuration =

            !durationFilter.value ||

            trek.duration == durationFilter.value

        return (

            matchesSearch &&

            matchesDifficulty &&

            matchesLocation &&

            matchesDuration

        )

    })

})

async function loadTreks() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/user/treks`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

    const data = await response.json()

    if (response.ok) {

        treks.value = data

    }
    else {

        alert(data.message || data.msg)

    }

}

async function bookTrek(trekId) {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/bookings`, {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            Authorization: `Bearer ${token}`

        },

        body: JSON.stringify({

            trek_id: trekId

        })

    })

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        loadTreks()

    }
    else {

        alert(data.message || data.msg)

    }

}
function logout(){

    localStorage.clear()

    router.push("/login")

}


onMounted(() => {

    loadTreks()

})

</script>