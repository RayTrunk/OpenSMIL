<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-bold">Media Library</h2>
      <label class="bg-primary hover:bg-opacity-90 text-white px-4 py-2 rounded-lg font-bold flex items-center space-x-2 transition-all cursor-pointer">
        <Upload :size="20" />
        <span>Upload Media</span>
        <input type="file" class="hidden" @change="handleFileUpload" multiple accept="image/*,video/*">
      </label>
    </div>

    <!-- Drop Zone -->
    <div 
      @dragover.prevent="dragOver = true" 
      @dragleave.prevent="dragOver = false" 
      @drop.prevent="handleDrop"
      :class="dragOver ? 'border-primary bg-primary/10' : 'border-slate-700 bg-slate-800/50'"
      class="border-2 border-dashed rounded-2xl p-12 text-center transition-all"
    >
      <div class="flex flex-col items-center space-y-4">
        <div class="p-4 bg-slate-700 rounded-full text-slate-400">
          <Image :size="48" />
        </div>
        <div>
          <p class="text-lg font-bold text-slate-300">Drag & drop your files here</p>
          <p class="text-sm text-slate-500">Supports JPG, PNG, MP4, and more (Max 100MB)</p>
        </div>
      </div>
    </div>

    <!-- Media Gallery -->
    <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
      <div v-for="i in 6" :key="i" class="aspect-square bg-slate-800 rounded-xl animate-pulse"></div>
    </div>
    <div v-else-if="mediaList.length === 0" class="text-center py-12 bg-slate-800 rounded-xl border border-slate-700 text-slate-500 italic">
      Your library is empty.
    </div>
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
      <div v-for="media in mediaList" :key="media.id" class="group relative bg-slate-800 rounded-xl border border-slate-700 overflow-hidden shadow-lg hover:border-primary transition-all">
        <!-- Preview -->
        <div class="aspect-square bg-slate-900 flex items-center justify-center overflow-hidden">
          <img v-if="media.media_type === 'image'" :src="'http://localhost:8000' + media.url" :alt="media.name" class="object-cover w-full h-full" />
          <div v-else class="text-primary flex flex-col items-center">
            <Video :size="40" />
            <span class="text-[10px] uppercase font-bold mt-1">Video</span>
          </div>
        </div>
        
        <!-- Info Overlay -->
        <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-3">
          <div class="flex justify-between items-center">
            <div class="truncate pr-2">
              <div class="text-xs font-bold truncate">{{ media.name }}</div>
              <div class="text-[10px] text-slate-400">{{ (media.size / 1024 / 1024).toFixed(2) }} MB</div>
            </div>
            <button @click="deleteMedia(media.id)" class="text-red-400 hover:text-red-300">
              <Trash2 :size="16" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Upload, Image, Video, Trash2, FileIcon } from 'lucide-vue-next'
import axios from 'axios'

const mediaList = ref([])
const loading = ref(true)
const dragOver = ref(false)

const token = localStorage.getItem('token')
const headers = { Authorization: `Bearer ${token}` }

const fetchMedia = async () => {
  loading.value = true
  try {
    const res = await axios.get('http://localhost:8000/api/v1/media/', { headers })
    mediaList.value = res.data
  } catch (err) {
    console.error('Failed to fetch media', err)
  } finally {
    loading.value = false
  }
}

const handleFileUpload = (event: any) => {
  const files = event.target.files
  if (files) uploadFiles(files)
}

const handleDrop = (event: any) => {
  dragOver.value = false
  const files = event.dataTransfer.files
  if (files) uploadFiles(files)
}

const uploadFiles = async (files: FileList) => {
  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', file.name.split('.')[0])
    
    try {
      await axios.post('http://localhost:8000/api/v1/media/', formData, {
        headers: { ...headers, 'Content-Type': 'multipart/form-data' }
      })
      fetchMedia()
    } catch (err) {
      console.error('Upload failed for', file.name, err)
    }
  }
}

const deleteMedia = async (id: number) => {
  if (confirm('Are you sure you want to delete this asset?')) {
    await axios.delete(`http://localhost:8000/api/v1/media/${id}`, { headers })
    fetchMedia()
  }
}

onMounted(fetchMedia)
</script>
