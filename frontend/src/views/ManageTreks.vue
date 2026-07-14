<template>

<div class="container mt-5">

    <h2 class="mb-4">Manage Treks</h2>

    <button
        class="btn btn-primary mb-3"
        @click="loadTreks"
    >
        Refresh Treks
    </button>

<div class="row mt-4 mb-3">

    <div class="col-md-6">

        <label class="form-label">
            Search Trek
        </label>

        <input
            type="text"
            class="form-control"
            placeholder="Search by name or location"
            v-model="search"
        >

    </div>

</div>


<h3 class="mb-4">Create Trek</h3>

<div class="row">

    <!-- Trek Name -->
    <div class="col-md-6 mb-3">
        <label class="form-label">Trek Name</label>
        <input
            type="text"
            class="form-control"
            v-model="name"
        >
    </div>

    <!-- Location -->
    <div class="col-md-6 mb-3">
        <label class="form-label">Location</label>
        <input
            type="text"
            class="form-control"
            v-model="location"
        >
    </div>

    <!-- Difficulty -->
    <div class="col-md-4 mb-3">
        <label class="form-label">Difficulty</label>

        <select
            class="form-select"
            v-model="difficulty"
        >
            <option value="">Select Difficulty</option>
            <option value="Easy">Easy</option>
            <option value="Moderate">Moderate</option>
            <option value="Hard">Hard</option>
        </select>
    </div>

    <!-- Duration -->
    <div class="col-md-4 mb-3">
        <label class="form-label">Duration (Days)</label>

        <input
            type="number"
            class="form-control"
            min="1"
            v-model="duration"
        >
    </div>

    <!-- Available Slots -->
    <div class="col-md-4 mb-3">
        <label class="form-label">Available Slots</label>

        <input
            type="number"
            class="form-control"
            min="1"
            v-model="available_slots"
        >
    </div>

    <!-- Assigned Staff -->
    <div class="col-md-6 mb-3">
        <label class="form-label">Assigned Staff</label>

        <select
            class="form-select"
            v-model="assigned_staff_id"
        >
            <option value="">Select Staff</option>

            <option
                v-for="staff in staffList"
                :key="staff.id"
                :value="staff.id"
            >
                {{ staff.name }}
            </option>

        </select>
    </div>

    <!-- Status -->
    <div class="col-md-6 mb-3">
        <label class="form-label">Status</label>

        <select
            class="form-select"
            v-model="status"
        >
            <option value="">Select Status</option>
            <option value="Pending">Pending</option>
            <option value="Approved">Approved</option>
            <option value="Open">Open</option>
            <option value="Closed">Closed</option>
            <option value="Completed">Completed</option>
        </select>
    </div>

    <!-- Start Date -->
    <div class="col-md-6 mb-3">
        <label class="form-label">Start Date</label>

        <input
            type="date"
            class="form-control"
            v-model="start_date"
        >
    </div>

    <!-- End Date -->
    <div class="col-md-6 mb-3">
        <label class="form-label">End Date</label>

        <input
            type="date"
            class="form-control"
            v-model="end_date"
        >
    </div>

    <!-- Description -->
    <div class="col-12 mb-3">
        <label class="form-label">Description</label>

        <textarea
            class="form-control"
            rows="3"
            v-model="description"
        ></textarea>
    </div>

</div>

<button
    class="btn btn-success"
    @click="editMode ? updateTrek() : createTrek()"
>
    {{ editMode ? "Update Trek" : "Create Trek" }}
</button>
    <table class="table table-bordered table-striped">

        <thead>

            <tr>
                <th>ID</th>
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
                <th>Actions</th>
            </tr>

        </thead>

        <tbody>

            <tr
                v-for="trek in filteredTreks"
                :key="trek.id"
            >

                <td>{{ trek.id }}</td>
                <td>{{ trek.name }}</td>
                <td>{{ trek.location }}</td>
                <td>{{ trek.difficulty }}</td>
                <td>{{ trek.duration }} days</td>
                <td>{{ trek.available_slots }}</td>
                <td>{{ trek.staff_name ? trek.staff_name : "Not Assigned" }}</td>
                <td>{{ trek.status }}</td>
                <td>{{ trek.start_date }}</td>
                <td>{{ trek.end_date }}</td>
                <td>{{ trek.description }}</td>


                <td>
                    <button
                        class="btn btn-warning btn-sm me-2"
                        @click="editTrek(trek)"
                    >
                        Edit
                    </button>
                    <button
                        class="btn btn-danger btn-sm"
                        @click="deleteTrek(trek.id)"
                    >
                        Delete
                    </button>
                </td>

            </tr>

        </tbody>

    </table>

</div>

</template>

<script setup>

import { ref, onMounted, computed } from "vue"
import { API_URL } from "../config"



const treks = ref([])
const name = ref("")
const location = ref("")
const difficulty = ref("")
const duration = ref("")
const available_slots = ref("")
const assigned_staff_id = ref("")
const status = ref("")
const start_date = ref("")
const end_date = ref("")
const description = ref("")
const staffList = ref([])

const editMode = ref(false)
const editingTrekId = ref(null)


const search = ref("")
const filteredTreks = computed(() => {

    if (!search.value.trim()) {

        return treks.value

    }

    const query = search.value.toLowerCase()

    return treks.value.filter(trek =>

        trek.name.toLowerCase().includes(query) ||
        trek.location.toLowerCase().includes(query)

    )

})



async function loadTreks() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/treks`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

        if (response.ok) {

            treks.value = await response.json()

        }
        else {

            alert("Failed to load treks.")

        }

}


async function loadStaff() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/staff`, {

        headers: {
            Authorization: `Bearer ${token}`
        }

    })

    if (response.ok) {

        staffList.value = await response.json()

    }
    else {

        alert("Failed to load staff.")

    }

}


function validateTrek() {

    if (
        !name.value ||
        !location.value ||
        !difficulty.value ||
        !duration.value ||
        !available_slots.value ||
        !status.value ||
        !start_date.value ||
        !end_date.value
    ) {

        alert("Please fill all required fields.")
        return false

    }

    const today = new Date().toISOString().split("T")[0]

    if (start_date.value < today) {

        alert("Start date cannot be in the past.")
        return false

    }

    if (end_date.value < start_date.value) {

        alert("End date cannot be before start date.")
        return false

    }

    return true

}





async function createTrek() {

   if (!validateTrek()) {
    return
        }

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/treks`, {

        method: "POST",

        headers: {

            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`

        },

        body: JSON.stringify({

            name: name.value,
            location: location.value,
            difficulty: difficulty.value,
            duration: Number(duration.value),
            available_slots: Number(available_slots.value),
            assigned_staff_id: assigned_staff_id.value || null,
            status: status.value,
            start_date: start_date.value,
            end_date: end_date.value,
            description: description.value

        })

    })

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        name.value = ""
        location.value = ""
        difficulty.value = ""
        duration.value = ""
        available_slots.value = ""
        assigned_staff_id.value = ""
        status.value = ""
        start_date.value = ""
        end_date.value = ""
        description.value = ""

        loadTreks()

    }
    else {

        alert(data.message)

    }

}



async function deleteTrek(id) {

    if (!confirm("Are you sure you want to delete this trek?")) {

        return

    }

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/treks/${id}`, {

        method: "DELETE",

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        loadTreks()

    }
    else {

        alert(data.message)

    }

}


function editTrek(trek) {

    editMode.value = true

    editingTrekId.value = trek.id

    name.value = trek.name
    location.value = trek.location
    difficulty.value = trek.difficulty
    duration.value = trek.duration
    available_slots.value = trek.available_slots
    assigned_staff_id.value = trek.assigned_staff_id || ""
    status.value = trek.status
    start_date.value = trek.start_date
    end_date.value = trek.end_date
    description.value = trek.description

}











async function updateTrek() {
    if (!validateTrek()) {
        return
    }

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/treks/${editingTrekId.value}`, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`

        },

        body: JSON.stringify({

            name: name.value,
            location: location.value,
            difficulty: difficulty.value,
            duration: Number(duration.value),
            available_slots: Number(available_slots.value),
            assigned_staff_id: assigned_staff_id.value || null,
            status: status.value,
            start_date: start_date.value,
            end_date: end_date.value,
            description: description.value

        })

    })

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        editMode.value = false
        editingTrekId.value = null

        name.value = ""
        location.value = ""
        difficulty.value = ""
        duration.value = ""
        available_slots.value = ""
        assigned_staff_id.value = ""
        status.value = ""
        start_date.value = ""
        end_date.value = ""
        description.value = ""

        loadTreks()

    }
    else {

        alert(data.message)

    }

}










onMounted(() => {

    loadTreks()
    loadStaff()

})
</script>