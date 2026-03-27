<template>
  <div class="min-h-screen flex bg-slate-900 text-white w-full">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 border-r border-slate-700 flex flex-col">
      <div class="p-6 flex items-center space-x-3 border-b border-slate-700">
        <img src="http://localhost:8000/static/logo.png" alt="Logo" class="h-8 w-auto" />
        <span class="font-bold text-lg tracking-tight">OpenSMIL</span>
      </div>
      <nav class="flex-1 p-4 space-y-2">
        <router-link to="/" class="flex items-center space-x-3 p-3 rounded-lg hover:bg-slate-700 transition-colors" :class="{ 'bg-primary text-white': $route.name === 'Dashboard' }">
          <LayoutDashboard :size="20" />
          <span>Dashboard</span>
        </router-link>
        <router-link to="/players" class="flex items-center space-x-3 p-3 rounded-lg hover:bg-slate-700 transition-colors" :class="{ 'bg-primary text-white': $route.name === 'Players' }">
          <Monitor :size="20" />
          <span>Players</span>
        </router-link>
        <router-link to="/media" class="flex items-center space-x-3 p-3 rounded-lg hover:bg-slate-700 transition-colors" :class="{ 'bg-primary text-white': $route.name === 'Media' }">
          <Image :size="20" />
          <span>Media</span>
        </router-link>
        <router-link to="/playlists" class="flex items-center space-x-3 p-3 rounded-lg hover:bg-slate-700 transition-colors" :class="{ 'bg-primary text-white': $route.name === 'Playlists' }">
          <PlaySquare :size="20" />
          <span>Playlists</span>
        </router-link>
      </nav>
      <div class="p-4 border-t border-slate-700">
        <button @click="logout" class="flex items-center space-x-3 p-3 w-full rounded-lg hover:bg-red-900/30 text-red-400 transition-colors">
          <LogOut :size="20" />
          <span>Logout</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col">
      <header class="h-16 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-8">
        <h1 class="text-xl font-semibold">{{ $route.name }}</h1>
        <div class="flex items-center space-x-4">
          <div class="h-8 w-8 rounded-full bg-primary flex items-center justify-center font-bold">A</div>
          <span class="text-sm font-medium text-slate-300">Administrator</span>
        </div>
      </header>
      <div class="p-8 overflow-y-auto flex-1">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { LayoutDashboard, Monitor, Image, PlaySquare, LogOut } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
@reference "../assets/style.css";

.router-link-active {
  @apply bg-primary text-white;
}
</style>
