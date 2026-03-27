<template>
  <div class="space-y-8">
    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="stat in stats" :key="stat.name" class="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
        <div class="flex items-center justify-between mb-4">
          <div class="p-3 bg-primary bg-opacity-10 rounded-lg text-primary">
            <component :is="stat.icon" :size="24" />
          </div>
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Total</span>
        </div>
        <div class="text-3xl font-bold">{{ stat.value }}</div>
        <div class="text-sm text-slate-400 mt-1">{{ stat.name }}</div>
      </div>
    </div>

    <!-- Overview & Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Player Status Overview -->
      <div class="bg-slate-800 rounded-xl border border-slate-700 shadow-lg overflow-hidden">
        <div class="p-6 border-b border-slate-700 flex items-center justify-between">
          <h3 class="font-bold text-lg">Active Players</h3>
          <button class="text-primary text-sm font-bold hover:underline">View All</button>
        </div>
        <div class="p-6">
          <div v-if="loading" class="animate-pulse space-y-4">
            <div v-for="i in 3" :key="i" class="h-12 bg-slate-700 rounded-lg"></div>
          </div>
          <div v-else-if="players.length === 0" class="text-center py-8 text-slate-500">
            No players found. Register your first device!
          </div>
          <div v-else class="space-y-4">
            <div v-for="player in players" :key="player.id" class="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg border border-slate-600">
              <div class="flex items-center space-x-4">
                <div class="h-10 w-10 rounded-full bg-slate-600 flex items-center justify-center">
                  <Monitor :size="20" />
                </div>
                <div>
                  <div class="font-bold">{{ player.name }}</div>
                  <div class="text-xs text-slate-400">{{ player.mac_address }}</div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span class="h-2 w-2 rounded-full" :class="player.is_active ? 'bg-green-500' : 'bg-red-500'"></span>
                <span class="text-xs font-bold uppercase tracking-tight">{{ player.is_active ? 'Online' : 'Offline' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Health -->
      <div class="bg-slate-800 rounded-xl border border-slate-700 shadow-lg overflow-hidden p-6 space-y-6">
        <h3 class="font-bold text-lg">System Status</h3>
        <div class="space-y-6">
          <div v-for="service in services" :key="service.name" class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="font-medium text-slate-300">{{ service.name }}</span>
              <span class="text-xs font-bold text-primary">{{ service.status }}</span>
            </div>
            <div class="w-full bg-slate-700 h-2 rounded-full overflow-hidden">
              <div class="bg-primary h-full transition-all duration-1000" :style="{ width: service.health + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Monitor, Image, PlaySquare, ShieldCheck, Activity } from 'lucide-vue-next'
import axios from 'axios'

const players = ref([])
const loading = ref(true)

const stats = ref([
  { name: 'Devices', value: '0', icon: Monitor },
  { name: 'Media Assets', value: '0', icon: Image },
  { name: 'Playlists', value: '0', icon: PlaySquare },
  { name: 'Uptime', value: '99.9%', icon: Activity }
])

const services = ref([
  { name: 'SMIL Engine', status: 'Operational', health: 100 },
  { name: 'Media Server', status: 'Healthy', health: 95 },
  { name: 'Database API', status: 'Online', health: 100 }
])

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const headers = { Authorization: `Bearer ${token}` }
    
    // Fetch data in parallel
    const [playersRes, mediaRes, playlistsRes] = await Promise.all([
      axios.get('http://localhost:8000/api/v1/players/', { headers }),
      axios.get('http://localhost:8000/api/v1/media/', { headers }),
      axios.get('http://localhost:8000/api/v1/playlists/', { headers })
    ])

    players.value = playersRes.data
    stats.value[0].value = playersRes.data.length.toString()
    stats.value[1].value = mediaRes.data.length.toString()
    stats.value[2].value = playlistsRes.data.length.toString()
  } catch (err) {
    console.error('Failed to fetch dashboard data', err)
  } finally {
    loading.value = false
  }
})
</script>
