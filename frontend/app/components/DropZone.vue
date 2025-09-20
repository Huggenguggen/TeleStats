<script setup lang="ts">
import { ref } from "vue"
import { useDropZone } from "@vueuse/core"
import { useRouter } from "vue-router"

const dropZoneRef = ref<HTMLElement | null>(null)
const files = ref<File[]>([])
const fileInputRef = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)
const errorMessage = ref<string | null>(null)

const router = useRouter()
const config = useRuntimeConfig()

function onDrop(droppedFiles: File[] | null) {
  if (droppedFiles) {
    files.value = droppedFiles
  }
}

const { isOverDropZone } = useDropZone(dropZoneRef, {
  onDrop,
  dataTypes: ["application/json"], // only accept .json files
})

function triggerFileInput() {
  fileInputRef.value?.click()
}

async function uploadFile() {
  if (files.value.length === 0) return

  const formData = new FormData()
  formData.append("file", files.value[0]) // only one file for now

  isUploading.value = true
  errorMessage.value = null

  try {
    const res = await $fetch<{ chat_id: number }>(
      `${config.public.apiBase}/api/chats/upload`,
      {
        method: "POST",
        body: formData,
      }
    )
    console.log("res.chat_id", res.chat_id)
    if (res.chat_id) {
      router.push(`/chat/${res.chat_id}`)
    }
  } catch (err: any) {
    errorMessage.value = err?.data?.error || "Upload failed"
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="w-full p-2">
    <!-- Drop Zone -->
    <div
      ref="dropZoneRef"
      class="flex flex-col items-center justify-center border-2 border-dashed rounded-2xl p-8 cursor-pointer transition-colors duration-200"
      :class="isOverDropZone ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'"
      @click="triggerFileInput"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-12 w-12 text-gray-400 mb-3"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6H16a5 5 0 011 9.9M12 12v9m0 0l-3-3m3 3l3-3"
        />
      </svg>
      <p class="text-gray-600 font-medium">Drag & drop your Telegram JSON here</p>
      <p class="text-sm text-gray-400 mt-1">or click to select</p>
      <input
        ref="fileInputRef"
        type="file"
        accept="application/json"
        class="hidden"
        @change="onDrop($event.target.files ? Array.from($event.target.files) : null)"
      />
    </div>

    <!-- File List -->
    <div v-if="files.length > 0" class="mt-6">
      <h3 class="text-lg font-semibold text-gray-700 mb-2">Selected File</h3>
      <ul class="space-y-1">
        <li
          v-for="file in files"
          :key="file.name"
          class="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-2 shadow-sm border border-gray-200"
        >
          <span class="text-gray-700">{{ file.name }}</span>
          <span class="text-xs text-gray-500">{{ (file.size / 1024).toFixed(1) }} KB</span>
        </li>
      </ul>

      <button
        @click="uploadFile"
        :disabled="isUploading"
        class="mt-4 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg shadow hover:bg-blue-700 disabled:opacity-50"
      >
        {{ isUploading ? "Uploading..." : "Upload & Analyze" }}
      </button>

      <p v-if="errorMessage" class="mt-2 text-red-600 text-sm">
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>
