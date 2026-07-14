<template>
    <div class="container mt-5">

        <div class="row justify-content-center">

            <div class="col-md-20">

                <div class="card p-7 shadow">

                    <h2 class="text-center mb-4">
                        Register
                    </h2>

                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input
                            class="form-control"
                            v-model="name"
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input
                            type="email"
                            class="form-control"
                            v-model="email"
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input
                            class="form-control"
                            v-model="phone"
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input
                            type="password"
                            class="form-control"
                            v-model="password"
                        >
                    </div>

                    <button
                        class="btn btn-success w-100"
                        @click="register"
                    >
                        Register
                    </button>

                    <p class="text-center mt-3 mb-0">
                        Already have an account?
                        <router-link to="/login">
                            Login
                        </router-link>
                    </p>

                </div>

            </div>

        </div>

    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { API_URL } from "../config"

const router = useRouter()

const name = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")

async function register() {

    const response = await fetch(`${API_URL}/register`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: name.value,
            email: email.value,
            phone: phone.value,
            password: password.value

        })

    })

    const data = await response.json()

    if (response.ok) {

        alert("Registration Successful")

        router.push("/login")

    }
    else {

        alert(data.message)

    }

}
</script>