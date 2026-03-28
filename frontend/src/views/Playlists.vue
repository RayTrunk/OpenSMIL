<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-bold">Playlists</h2>
      <button @click="showAddModal = true" class="bg-primary hover:bg-opacity-90 text-white px-4 py-2 rounded-lg font-bold flex items-center space-x-2 transition-all">
        <Plus :size="20" />
        <span>New Playlist</span>
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="playlist in playlists" :key="playlist.id" class="bg-slate-800 rounded-xl border border-slate-700 shadow-lg overflow-hidden flex flex-col">
        <div class="p-6 border-b border-slate-700">
          <h3 class="font-bold text-lg flex items-center space-x-2">
            <PlaySquare :size="20" class="text-primary" />
            <span>{{ playlist.name }}</span>
          </h3>
          <p class="text-xs text-slate-500 mt-1">{{ playlist.description || 'No description' }}</p>
        </div>
        
        <!-- Playlist Items Summary -->
        <div class="flex-1 p-6">
           <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Content ({{ playlist.items?.length || 0 }})</div>
           <div class="space-y-2">
             <div v-for="item in playlist.items?.slice(0, 3)" :key="item.id" class="flex items-center space-x-3 text-sm text-slate-300">
               <Image v-if="item.media?.media_type === 'image'" :size="14" />
               <Video v-else :size="14" />
               <span class="truncate">{{ item.media?.name }}</span>
               <span class="text-[10px] text-slate-500 ml-auto">{{ item.duration }}s</span>
             </div>
             <div v-if="!playlist.items || playlist.items.length === 0" class="text-sm text-slate-600 italic">Empty playlist</div>
             <div v-if="playlist.items?.length > 3" class="text-[10px] text-primary font-bold">+ {{ playlist.items.length - 3 }} more</div>
           </div>
        </div>

        <div class="p-4 bg-slate-700/30 border-t border-slate-700 flex space-x-2 mt-auto">
          <button @click="editPlaylist(playlist)" class="flex-1 bg-slate-700 hover:bg-slate-600 text-xs font-bold py-2 rounded-lg transition-all">Manage Content</button>
          <button @click="deletePlaylist(playlist.id)" class="bg-red-900/20 hover:bg-red-900/40 text-red-400 p-2 rounded-lg transition-all"><Trash2 :size="18" /></button>
        </div>
      </div>
    </div>

    <!-- Create Playlist Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-slate-800 w-full max-w-md rounded-2xl shadow-2xl border border-slate-700 overflow-hidden">
        <div class="p-6 border-b border-slate-700 flex justify-between items-center">
          <h3 class="text-xl font-bold">New Playlist</h3>
          <button @click="showAddModal = false" class="text-slate-400 hover:text-white"><X :size="24" /></button>
        </div>
        <form @submit.prevent="createPlaylist" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">Playlist Name</label>
            <input v-model="newPlaylist.name" type="text" required class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:ring-primary focus:border-primary outline-none" placeholder="Lobby Loop">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">Description</label>
            <textarea v-model="newPlaylist.description" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:ring-primary focus:border-primary outline-none" rows="3" placeholder="Morning welcome messages..."></textarea>
          </div>
          <div class="pt-4 flex space-x-3">
            <button type="button" @click="showAddModal = false" class="flex-1 bg-slate-700 hover:bg-slate-600 py-2 rounded-lg font-bold transition-all">Cancel</button>
            <button type="submit" class="flex-1 bg-primary hover:bg-opacity-90 py-2 rounded-lg font-bold transition-all">Create</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Playlist Content Editor (Advanced) -->
    <div v-if="selectedPlaylist" class="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50 p-4 lg:p-12">
      <div class="bg-slate-800 w-full max-w-6xl h-full rounded-2xl shadow-2xl border border-slate-700 overflow-hidden flex flex-col">
        <div class="p-6 border-b border-slate-700 flex justify-between items-center">
          <div>
            <h3 class="text-2xl font-bold">Edit Playlist: {{ selectedPlaylist.name }}</h3>
            <p class="text-sm text-slate-400">Add media and set durations</p>
          </div>
          <button @click="selectedPlaylist = null" class="bg-slate-700 hover:bg-slate-600 p-2 rounded-full"><X :size="24" /></button>
        </div>
        
        <div class="flex-1 flex overflow-hidden">
          <!-- Left: Library -->
          <div class="w-1/3 border-r border-slate-700 p-6 overflow-y-auto space-y-4">
            <h4 class="font-bold text-sm uppercase tracking-widest text-slate-500">Available Media</h4>
            <div class="grid grid-cols-2 gap-4">
              <div v-for="media in mediaLibrary" :key="media.id" @click="addToPlaylist(media)" class="group cursor-pointer bg-slate-700 rounded-lg overflow-hidden border border-transparent hover:border-primary transition-all">
                <div class="aspect-video relative overflow-hidden bg-slate-900 flex items-center justify-center">
                  <img v-if="media.media_type === 'image'" :src="'http://localhost:8000' + media.url" class="object-cover w-full h-full" />
                  <Video v-else :size="24" class="text-primary" />
                  <div class="absolute inset-0 bg-primary/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <Plus :size="24" />
                  </div>
                </div>
                <div class="p-2 text-[10px] font-bold truncate">{{ media.name }}</div>
              </div>
            </div>
          </div>
          
          <!-- Right: Sequence -->
          <div class="flex-1 p-6 overflow-y-auto">
            <h4 class="font-bold text-sm uppercase tracking-widest text-slate-500 mb-6">Playback Sequence</h4>
            <div class="space-y-4">
              <div v-for="(item, index) in selectedPlaylist.items" :key="index" class="flex items-center space-x-4 bg-slate-700/50 p-4 rounded-xl border border-slate-600">
                <div class="text-xl font-black text-slate-600 w-8">{{ index + 1 }}</div>
                <div class="h-16 w-24 bg-slate-900 rounded-lg overflow-hidden flex-shrink-0">
                   <img v-if="item.media?.media_type === 'image'" :src="'http://localhost:8000' + item.media.url" class="object-cover w-full h-full" />
                   <div v-else class="w-full h-full flex items-center justify-center text-primary"><Video :size="24" /></div>
                </div>
                <div class="flex-1">
                   <div class="font-bold">{{ item.media?.name }}</div>
                   <div class="text-xs text-slate-400">{{ item.media?.media_type }}</div>
                </div>
                <div class="flex items-center space-x-3">
                  <div class="flex flex-col">
                    <label class="text-[10px] text-slate-500 font-bold uppercase">Duration (s)</label>
                    <input v-model="item.duration" type="number" class="bg-slate-800 border border-slate-600 rounded p-1 w-16 text-center text-sm">
                  </div>
                  <button @click="removeItem(index)" class="text-red-400 hover:text-red-300 p-2"><Trash2 :size="18" /></button>
                </div>
              </div>
              <div v-if="!selectedPlaylist.items || selectedPlaylist.items.length === 0" class="text-center py-12 border-2 border-dashed border-slate-700 rounded-2xl text-slate-600">
                Click on media from the left to build your loop.
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-6 border-t border-slate-700 flex justify-end">
           <button @click="savePlaylistContent" class="bg-primary hover:bg-opacity-90 px-8 py-3 rounded-xl font-bold transition-all">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, PlaySquare, Trash2, X, Image, Video, MoreVertical } from 'lucide-vue-next'
import axios from 'axios'

const playlists = ref([])
const mediaLibrary = ref([])
const showAddModal = ref(false)
const selectedPlaylist = ref(null)
const newPlaylist = ref({ name: '', description: '' })

const token = localStorage.getItem('token')
const headers = { Authorization: `Bearer ${token}` }

const fetchPlaylists = async () => {
  const res = await axios.get('http://localhost:8000/api/v1/playlists/', { headers })
  playlists.value = res.data
}

const fetchMedia = async () => {
  const res = await axios.get('http://localhost:8000/api/v1/media/', { headers })
  mediaLibrary.value = res.data
}

const createPlaylist = async () => {
  await axios.post('http://localhost:8000/api/v1/playlists/', newPlaylist.value, { headers })
  showAddModal.value = false
  newPlaylist.value = { name: '', description: '' }
  fetchPlaylists()
}

const deletePlaylist = async (id: number) => {
  if (confirm('Delete this playlist?')) {
    await axios.delete(`http://localhost:8000/api/v1/playlists/${id}`, { headers })
    fetchPlaylists()
  }
}

const editPlaylist = (playlist: any) => {
  // Deep copy for editing
  selectedPlaylist.value = JSON.parse(JSON.stringify(playlist))
  if (!selectedPlaylist.value.items) selectedPlaylist.value.items = []
}

const addToPlaylist = (media: any) => {
  selectedPlaylist.value.items.push({
    media_id: media.id,
    media: media,
    duration: 10,
    position: selectedPlaylist.value.items.length
  })
}

const removeItem = (index: number) => {
  selectedPlaylist.value.items.splice(index, 1)
}

const savePlaylistContent = async () => {
  try {
     // 1. Delete old items first (simplified approach: delete all and re-add or handle properly)
     // For this version, we'll just add new items that don't have an ID
     // and cleanup the payload sent to backend
     for (const item of selectedPlaylist.value.items) {
       if (!item.id) {
         const payload = {
           media_id: item.media_id,
           duration: item.duration,
           position: item.position
         }
         await axios.post(`http://localhost:8000/api/v1/playlists/${selectedPlaylist.value.id}/items`, payload, { headers })
       }
     }
     selectedPlaylist.value = null
     fetchPlaylists()
  } catch (err) {
    console.error('Failed to save playlist', err)
    alert('Failed to save playlist content.')
  }
}

onMounted(() => {
  fetchPlaylists()
  fetchMedia()
})
</script>
