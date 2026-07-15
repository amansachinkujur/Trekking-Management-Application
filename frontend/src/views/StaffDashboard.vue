<template>

<!-- Staff dashboard content -->
<div class="container mt-5">

    <h2 class="mb-4">
        Staff Dashboard
    </h2>

    <!-- Page actions -->
    <button
        class="btn btn-primary mb-3"
        @click="loadTreks"
    >
        Refresh Treks
    </button>

    <button
        class="btn btn-danger mb-3 ms-2"
        @click="logout"
    >
        Logout
    </button>

    <!-- Search section -->
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

    </div>

    <h3 class="mb-4">
        Assigned Treks
    </h3>

    <!-- Assigned treks table -->
    <table class="table table-bordered table-striped">

        <thead>

            <tr>

                <th>Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Duration</th>
                <th>Available Slots</th>
                <th>Registered Users</th>
                <th>Status</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Actions</th>

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
                <td>{{ trek.registered_users }}</td>
                <td>{{ trek.status }}</td>

                <td>{{ trek.start_date }}</td>

                <td>{{ trek.end_date }}</td>

                <td>

                    <button
                        class="btn btn-warning btn-sm me-2"
                        @click="editTrek(trek)"
                    >
                        Edit
                    </button>

                    <button
                        class="btn btn-info btn-sm"
                        @click="viewParticipants(trek.id)"
                    >
                        Participants
                    </button>

                </td>

            </tr>

        </tbody>

    </table>

    <!-- Edit trek section -->
    <h3
        v-if="editMode"
        class="mt-5 mb-4"
    >
        Update Trek
    </h3>

    <div
        v-if="editMode"
        class="row"
    >

        <div class="col-md-6 mb-3">

            <label class="form-label">
                Available Slots
            </label>

            <input
                type="number"
                class="form-control"
                min="0"
                v-model="available_slots"
            >

        </div>

        <div class="col-md-6 mb-3">

            <label class="form-label">
                Status
            </label>

            <select
                class="form-select"
                v-model="status"
            >

                <option value="Open">
                    Open
                </option>

                <option value="Closed">
                    Closed
                </option>

                <option value="Completed">
                    Completed
                </option>

            </select>

        </div>

    </div>

    <button
        v-if="editMode"
        class="btn btn-success"
        @click="updateTrek"
    >
        Update Trek
    </button>

</div>

</template>


<script setup>

// Vue imports and API config
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import { API_URL } from "../config"

// Router and trek state
const router = useRouter()

const treks = ref([])

const search = ref("")

const editMode = ref(false)

const editingTrekId = ref(null)

const available_slots = ref("")

const status = ref("")

// Filter treks by search text
const filteredTreks = computed(() => {

    if (!search.value.trim()) {

        return treks.value

    }

    const query = search.value.toLowerCase()

    return treks.value.filter(trek =>

        trek.name.toLowerCase().includes(query)

    )

})

// Load treks from API
async function loadTreks() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/staff/treks`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

    const data = await response.json()

    if (response.ok) {

        treks.value = data

    }
    else {

        alert(data.message)

    }

}

// Prepare trek for editing
function editTrek(trek) {

    editMode.value = true

    editingTrekId.value = trek.id

    available_slots.value = trek.available_slots

    status.value = trek.status

}

// Update trek details to API
async function updateTrek() {

    const token = localStorage.getItem("token")

    const response = await fetch(

        `${API_URL}/staff/treks/${editingTrekId.value}`,

        {

            method: "PUT",

            headers: {

                "Content-Type": "application/json",

                Authorization: `Bearer ${token}`

            },

            body: JSON.stringify({

                available_slots: Number(available_slots.value),

                status: status.value

            })

        }

    )

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        editMode.value = false

        editingTrekId.value = null

        loadTreks()

    }
    else {

        alert(data.message)

    }

}

// Navigate to trek participants page
function viewParticipants(trekId) {

    router.push(`/staff/treks/${trekId}/participants`)

}

// Clear session and return to login
function logout() {

    localStorage.clear()

    router.push("/login")

}

// Load treks on page mount
onMounted(() => {

    loadTreks()

})

</script>