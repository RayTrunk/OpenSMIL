<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-900 px-4">
    <div class="max-w-md w-full space-y-8 bg-slate-800 p-10 rounded-2xl shadow-2xl border border-slate-700">
      <div class="flex flex-col items-center">
        <img src="http://localhost:8000/static/logo.png" alt="OpenSMIL Logo" class="h-24 w-auto mb-6" />
        <h2 class="text-3xl font-extrabold text-white text-center">OpenSMIL Signage</h2>
        <p class="mt-2 text-sm text-slate-400">Sign in to your account</p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label class="text-slate-300 text-sm font-medium mb-1 block">Username</label>
            <input v-model="username" type="text" required class="appearance-none rounded-lg relative block w-full px-3 py-3 border border-slate-600 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm" placeholder="admin">
          </div>
          <div>
            <label class="text-slate-300 text-sm font-medium mb-1 block">Password</label>
            <input v-model="password" type="password" required class="appearance-none rounded-lg relative block w-full px-3 py-3 border border-slate-600 bg-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm" placeholder="••••••••">
          </div>
        </div>

        <div>
          <button type="submit" :disabled="loading" class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-lg text-white bg-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all disabled:opacity-50">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </div>
        <p v-if="error" class="text-red-400 text-sm text-center">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('admin')
const password = ref('admin')
const loading = ref(false)
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  loading.ref = true
  error.value = ''
  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const response = await axios.post('http://localhost:8000/api/v1/login/access-token', formData)
    localStorage.setItem('token', response.data.access_token)
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>
