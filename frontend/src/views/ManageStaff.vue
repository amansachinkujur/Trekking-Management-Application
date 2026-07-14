<template>

<div class="container mt-5">

    <h2 class="mb-4">Manage Staff</h2>

    <button
        class="btn btn-primary mb-3"
        @click="loadStaff"
    >
        Refresh Staff
    </button>

    <!-- Search -->

    <div class="row mt-4 mb-3">

        <div class="col-md-6">

            <label class="form-label">
                Search Staff
            </label>

            <input
                type="text"
                class="form-control"
                placeholder="Search by name or email"
                v-model="search"
            >

        </div>

    </div>

    <!-- Create / Update Staff -->

    <h3 class="mb-4">

        {{ editMode ? "Update Staff" : "Create Staff" }}

    </h3>

    <div class="row">

        <!-- Name -->

        <div class="col-md-6 mb-3">

            <label class="form-label">

                Name

            </label>

            <input
                type="text"
                class="form-control"
                v-model="name"
            >

        </div>

        <!-- Email -->

        <div class="col-md-6 mb-3">

            <label class="form-label">

                Email

            </label>

            <input
                type="email"
                class="form-control"
                v-model="email"
            >

        </div>

        <!-- Phone -->

        <div class="col-md-6 mb-3">

            <label class="form-label">

                Phone

            </label>

            <input
                type="text"
                class="form-control"
                v-model="phone"
            >

        </div>

        <!-- Password -->

        <div class="col-md-6 mb-3">

            <label class="form-label">

                Password

            </label>

            <input
                type="password"
                class="form-control"
                 placeholder="Leave blank to keep current password"
                v-model="password"
            >

        </div>

        <!-- Active -->

        <div class="col-md-6 mb-3">

            <label class="form-label">

                Status

            </label>

            <select
                class="form-select"
                v-model="is_active"
            >

                <option :value="true">

                    Active

                </option>

                <option :value="false">

                    Inactive

                </option>

            </select>

        </div>

    </div>

    <button
        class="btn btn-success"
        @click="editMode ? updateStaff() : createStaff()"
    >

        {{ editMode ? "Update Staff" : "Create Staff" }}

    </button>

    <!-- Table -->

    <table class="table table-bordered table-striped mt-4">

        <thead>

            <tr>

                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Status</th>
                <th>Actions</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="staff in filteredStaff"
                :key="staff.id"
            >

                <td>{{ staff.id }}</td>

                <td>{{ staff.name }}</td>

                <td>{{ staff.email }}</td>

                <td>{{ staff.phone }}</td>

                <td>

                    {{ staff.is_active ? "Active" : "Inactive" }}

                </td>

                <td>

                    <button
                        class="btn btn-warning btn-sm me-2"
                        @click="editStaff(staff)"
                    >

                        Edit

                    </button>

                    <button
                        class="btn btn-danger btn-sm"
                        @click="deleteStaff(staff.id)"
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

import { ref, computed, onMounted } from "vue"
import { API_URL } from "../config"

const staffList = ref([])

const name = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")
const is_active = ref(true)

const search = ref("")

const editMode = ref(false)
const editingStaffId = ref(null)

const filteredStaff = computed(() => {

    if (!search.value.trim()) {

        return staffList.value

    }

    const query = search.value.toLowerCase()

    return staffList.value.filter(staff =>

        staff.name.toLowerCase().includes(query) ||
        staff.email.toLowerCase().includes(query)

    )

})

function validateStaff() {

    if (

        !name.value ||
        !email.value

    ) {

        alert("Name and Email are required.")
        return false

    }

    if (

        !editMode.value &&
        !password.value

    ) {

        alert("Password is required.")
        return false

    }

    return true

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

function clearForm() {

    name.value = ""
    email.value = ""
    phone.value = ""
    password.value = ""
    is_active.value = true

    editMode.value = false
    editingStaffId.value = null

}

async function createStaff() {

    if (!validateStaff()) {

        return

    }

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/staff`, {

        method: "POST",

        headers: {

            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`

        },

        body: JSON.stringify({

            name: name.value,
            email: email.value,
            phone: phone.value,
            password: password.value,
            is_active: is_active.value

        })

    })

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        clearForm()

        loadStaff()

    }
    else {

        alert(data.message)

    }

}

function editStaff(staff) {

    editMode.value = true

    editingStaffId.value = staff.id

    name.value = staff.name
    email.value = staff.email
    phone.value = staff.phone || ""
    password.value = ""
    is_active.value = staff.is_active

}

async function updateStaff() {

    if (!validateStaff()) {

        return

    }

    const token = localStorage.getItem("token")

    const body = {

        name: name.value,
        email: email.value,
        phone: phone.value,
        is_active: is_active.value

    }

    if (password.value) {

        body.password = password.value

    }

    const response = await fetch(

        `${API_URL}/staff/${editingStaffId.value}`,

        {

            method: "PUT",

            headers: {

                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`

            },

            body: JSON.stringify(body)

        }

    )

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        clearForm()

        loadStaff()

    }
    else {

        alert(data.message)

    }

}

async function deleteStaff(id) {

    if (!confirm("Are you sure you want to delete this staff member?")) {

        return

    }

    const token = localStorage.getItem("token")

    const response = await fetch(

        `${API_URL}/staff/${id}`,

        {

            method: "DELETE",

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    )

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        loadStaff()

    }
    else {

        alert(data.message)

    }

}

onMounted(() => {

    loadStaff()

})

</script>