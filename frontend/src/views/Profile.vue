<template>

<!-- Profile page content -->
<div class="container mt-5">

    <h2 class="mb-4">
        My Profile
    </h2>

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

        <!-- New Password -->

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

    </div>

    <!-- Profile actions -->
    <button
        class="btn btn-success"
        @click="updateProfile"
    >
        Update Profile
    </button>

</div>

</template>


<script setup>

// Vue imports and API config
import { ref, onMounted } from "vue"
import { API_URL } from "../config"

// Profile form state
const name = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")

// Load profile from API
async function loadProfile() {

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/profile`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    })

    const data = await response.json()

    if (response.ok) {

        name.value = data.name
        email.value = data.email
        phone.value = data.phone || ""

    }
    else {

        alert(data.message)

    }

}

// Update profile to API
async function updateProfile() {

    if (

        !name.value ||

        !email.value

    ) {

        alert("Name and Email are required.")

        return

    }

    const token = localStorage.getItem("token")

    const body = {

        name: name.value,
        email: email.value,
        phone: phone.value

    }

    if (password.value) {

        body.password = password.value

    }

    const response = await fetch(`${API_URL}/profile`, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json",

            Authorization: `Bearer ${token}`

        },

        body: JSON.stringify(body)

    })

    const data = await response.json()

    if (response.ok) {

        alert(data.message)

        password.value = ""

        loadProfile()

    }
    else {

        alert(data.message)

    }

}

// Load profile on page mount
onMounted(() => {

    loadProfile()

})

</script>
