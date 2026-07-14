


<template>
    <div class="container mt-10">

        <div class="row justify-content-center">

            <div class="col-md-10">

                <div class="card shadow">

                    <div class="card-body">

                        <h2 class="text-center mb-4">
                            Trekking Management System
                        </h2>

                        <div class="mb-3">

                            <label class="form-label">
                                Email
                            </label>

                            <input
                                type="email"
                                class="form-control"
                                v-model="email"
                            >

                        </div>

                        <div class="mb-3">

                            <label class="form-label">
                                Password
                            </label>

                            <input
                                type="password"
                                class="form-control"
                                v-model="password"
                            >

                        </div>

                        <button
                            class="btn btn-primary w-100"
                            @click="login"
                        >
                            Login
                        </button>

                        <p class="text-center mt-3">

                            Don't have an account?

                            <router-link to="/register">
                                Register
                            </router-link>

                        </p>

                    </div>

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

const email = ref("")
const password = ref("")

async function login() {

    const response = await fetch(`${API_URL}/login`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            email: email.value,
            password: password.value

        })

    })

    const data = await response.json()

    if (response.ok) {

        localStorage.setItem("token", data.access_token)
        localStorage.setItem("role", data.role)
        localStorage.setItem("name", data.name)

        if (data.role === "admin") {
            router.push("/admin")
        }
        else if (data.role === "staff") {
            router.push("/staff")
        }
        else {
            router.push("/user")
        }

    }
    else {

        alert(data.message)

    }



}

</script>