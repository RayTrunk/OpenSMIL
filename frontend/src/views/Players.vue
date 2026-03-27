<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-bold">Player Management</h2>
      <button @click="showAddModal = true" class="bg-primary hover:bg-opacity-90 text-white px-4 py-2 rounded-lg font-bold flex items-center space-x-2 transition-all">
        <Plus :size="20" />
        <span>Add Player</span>
      </button>
    </div>

    <!-- Player Table -->
    <div class="bg-slate-800 rounded-xl border border-slate-700 shadow-lg overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-700/50 text-slate-400 text-xs uppercase tracking-wider">
          <tr>
            <th class="p-4 border-b border-slate-700">Name</th>
            <th class="p-4 border-b border-slate-700">MAC Address</th>
            <th class="p-4 border-b border-slate-700">Assigned Playlist</th>
            <th class="p-4 border-b border-slate-700">Last Seen</th>
            <th class="p-4 border-b border-slate-700">Status</th>
            <th class="p-4 border-b border-slate-700 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-700">
          <tr v-for="player in players" :key="player.id" class="hover:bg-slate-700/30 transition-colors">
            <td class="p-4">
              <div class="font-bold">{{ player.name }}</div>
              <div class="text-xs text-slate-500">{{ player.description || 'No description' }}</div>
            </td>
            <td class="p-4 font-mono text-sm">{{ player.mac_address }}</td>
            <td class="p-4">
              <select @change="updatePlayerPlaylist(player, $event)" class="bg-slate-700 border border-slate-600 text-white text-sm rounded-lg focus:ring-primary focus:border-primary block w-full p-2">
                <option value="">No Playlist</option>
                <option v-for="pl in playlists" :key="pl.id" :value="pl.id" :selected="player.playlist_id === pl.id">
                  {{ pl.name }}
                </option>
              </select>
            </td>
            <td class="p-4 text-sm text-slate-400">
              {{ player.last_seen ? new Date(player.last_seen).toLocaleString() : 'Never' }}
            </td>
            <td class="p-4">
              <span :class="player.is_active ? 'bg-green-500/20 text-green-500' : 'bg-red-500/20 text-red-500'" class="px-2 py-1 rounded-full text-xs font-bold uppercase tracking-tight">
                {{ player.is_active ? 'Online' : 'Offline' }}
              </span>
            </td>
            <td class="p-4 text-right">
              <button @click="deletePlayer(player.id)" class="text-red-400 hover:text-red-300 transition-colors p-2">
                <Trash2 :size="18" />
              </button>
            </td>
          </tr>
          <tr v-if="players.length === 0">
            <td colspan="6" class="p-8 text-center text-slate-500 italic">No players registered.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Player Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-slate-800 w-full max-w-md rounded-2xl shadow-2xl border border-slate-700 overflow-hidden">
        <div class="p-6 border-b border-slate-700 flex justify-between items-center">
          <h3 class="text-xl font-bold">Register New Player</h3>
          <button @click="showAddModal = false" class="text-slate-400 hover:text-white"><X :size="24" /></button>
        </div>
        <form @submit.prevent="addPlayer" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">Display Name</label>
            <input v-model="newPlayer.name" type="text" required class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:ring-primary focus:border-primary outline-none" placeholder="Lobby Display 01">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">MAC Address</label>
            <input v-model="newPlayer.mac_address" type="text" required class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:ring-primary focus:border-primary outline-none font-mono" placeholder="AA:BB:CC:DD:EE:FF">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">Description (Optional)</label>
            <textarea v-model="newPlayer.description" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:ring-primary focus:border-primary outline-none" rows="3" placeholder="Located at the main entrance..."></textarea>
          </div>
          <div class="pt-4 flex space-x-3">
            <button type="button" @click="showAddModal = false" class="flex-1 bg-slate-700 hover:bg-slate-600 py-2 rounded-lg font-bold transition-all">Cancel</button>
            <button type="submit" class="flex-1 bg-primary hover:bg-opacity-90 py-2 rounded-lg font-bold transition-all">Register</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Trash2, X, Monitor } from 'lucide-vue-next'
import axios from 'axios'

const players = ref([])
const playlists = ref([])
const showAddModal = ref(false)
const newPlayer = ref({ name: '', mac_address: '', description: '' })

const token = localStorage.getItem('token')
const headers = { Authorization: `Bearer ${token}` }

const fetchPlayers = async () => {
  const res = await axios.get('http://localhost:8000/api/v1/players/', { headers })
  players.value = res.data
}

const fetchPlaylists = async () => {
  const res = await axios.get('http://localhost:8000/api/v1/playlists/', { headers })
  playlists.value = res.data
}

const addPlayer = async () => {
  try {
    await axios.post('http://localhost:8000/api/v1/players/', newPlayer.value, { headers })
    showAddModal.value = false
    newPlayer.value = { name: '', mac_address: '', description: '' }
    fetchPlayers()
  } catch (err) {
    alert('Failed to register player. Check MAC address uniqueness.')
  }
}

const deletePlayer = async (id: number) => {
  if (confirm('Are you sure you want to delete this player?')) {
    // Note: Backend needs delete endpoint if not already there, adding it here for completeness
    await axios.delete(`http://localhost:8000/api/v1/players/${id}`, { headers })
    fetchPlayers()
  }
}

// TODO: Implement actual player-to-playlist assignment logic in backend if missing
const updatePlayerPlaylist = async (player: any, event: any) => {
  const playlistId = event.target.value
  try {
    // In a real app, you'd have a PATCH /players/{id} endpoint
    await axios.put(`http://localhost:8000/api/v1/players/${player.id}`, { ...player, playlist_id: playlistId || null }, { headers })
    player.playlist_id = playlistId || null
  } catch (err) {
    console.error('Failed to update playlist', err)
  }
}

onMounted(() => {
  fetchPlayers()
  fetchPlaylists()
})
</script>
