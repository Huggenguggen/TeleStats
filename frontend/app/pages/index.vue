<script setup lang="ts">
import { ref } from "vue"
import ChatSearch from "~/components/ChatSearch.vue"

const file = ref<File | null>(null)
const config = useRuntimeConfig()

async function uploadFile() {
  if (!file.value) return
  const formData = new FormData()
  formData.append("file", file.value)

  const res = await $fetch(`${config.public.apiBase}/chats/upload`, {
    method: "POST",
    body: formData,
  })

  alert("Chat uploaded with ID: " + res.chat_id)
}
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Upload Telegram Chat exports (JSON only)</h1>
    <DropZone />
    <ChatSearch />
  </div>
</template>
