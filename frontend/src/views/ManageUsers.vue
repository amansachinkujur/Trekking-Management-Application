<template>

<!-- User management page -->
<div class="container mt-5">

    <h2 class="mb-4">
        Manage Users
    </h2>

    <button
        class="btn btn-primary mb-3"
        @click="loadUsers"
    >
        Refresh Users
    </button>

    <!-- Search users -->

    <div class="row mb-4">

        <div class="col-md-6">

            <label class="form-label">
                Search User
            </label>

            <input
                type="text"
                class="form-control"
                placeholder="Search by name or email"
                v-model="search"
            >

        </div>

    </div>

    <!-- Edit user form -->

    <h3 class="mb-4">
        Edit User
    </h3>

    <div class="row">

        <!-- Name field -->

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

        <!-- Email field -->

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

        <!-- Phone field -->

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

        <!-- New password field -->

        <div class="col-md-6 mb-3">

            <label class="form-label">
                New Password
            </label>

            <input
                type="password"
                class="form-control"
                placeholder="Leave blank to keep current password"
                v-model="password"
            >

        </div>

        <!-- Status field -->

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
        @click="updateUser"
    >
        Update User
    </button>

    <!-- User list table -->

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
                v-for="user in filteredUsers"
                :key="user.id"
            >

                <td>{{ user.id }}</td>

                <td>{{ user.name }}</td>

                <td>{{ user.email }}</td>

                <td>{{ user.phone }}</td>

                <td>

                    {{ user.is_active ? "Active" : "Inactive" }}

                </td>

                <td>

                    <button
                        class="btn btn-warning btn-sm"
                        @click="editUser(user)"
                    >
                        Edit
                    </button>

                </td>

            </tr>

        </tbody>

    </table>

</div>

</template>



<script setup>

// Vue imports and API config
import { ref, computed, onMounted } from "vue"
import { API_URL } from "../config"

// Form state and user data
const users = ref([])

const name = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")
const is_active = ref(true)

const search = ref("")

const editingUserId = ref(null)

// Filter users by search text
const filteredUsers = computed(() => {

    if (!search.value.trim()) {

        return users.value

    }

    const query = search.value.toLowerCase()

    return users.value.filter(user =>

        user.name.toLowerCase().includes(query) ||

        user.email.toLowerCase().includes(query)

    )

})

// Validate required user fields
function validateUser() {

    if (

        !name.value ||

        !email.value

    ) {

        alert("Name and Email are required.")

        return false

    }

    return true

}

// Reset form values
function clearForm() {

    name.value = ""
    email.value = ""
    phone.value = ""
    password.value = ""
    is_active.value = true

    editingUserId.value = null

}

// Load users from API
async function loadUsers() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/admin/users`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

    const data = await response.json()

    if (response.ok) {

        users.value = data

    }
    else {

        alert(data.message || data.msg)

    }

}

// Fill form for editing
function editUser(user) {

    editingUserId.value = user.id

    name.value = user.name
    email.value = user.email
    phone.value = user.phone || ""
    password.value = ""
    is_active.value = user.is_active

}

// Update existing user
async function updateUser() {

    if (!validateUser()) {

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

        `${API_URL}/admin/users/${editingUserId.value}`,

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

        loadUsers()

    }
    else {

        alert(data.message || data.msg)

    }

}

// Load users on page start
onMounted(() => {

    loadUsers()

})

</script>