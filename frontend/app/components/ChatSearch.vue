<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

const config = useRuntimeConfig()
const router = useRouter()

const chats = ref<any[]>([])
const search = ref("")

// Fetch chats
onMounted(async () => {
  chats.value = await $fetch(`${config.public.apiBase}/api/chats`)
})

// Filtered chats
const filteredChats = computed(() =>
  chats.value.filter((c) =>
    c.name?.toLowerCase().includes(search.value.toLowerCase()) ||
    String(c.id).includes(search.value)
  )
)

// Navigate to selected chat
function goToChat(id: string | number) {
  router.push(`/chat/${id}`)
}
</script>

<template>
  <div>
    <input
      v-model="search"
      type="text"
      placeholder="Search chats..."
      class="border rounded p-2 w-full text-black"
      @keyup.enter="search && goToChat(search)"
    />

    <ul
      v-if="search"
      class="absolute mt-1 w-1/3 bg-white text-black border rounded shadow-lg max-h-60 overflow-y-auto z-50"
    >
      <li
        v-for="chat in filteredChats"
        :key="chat.id"
        class="p-2 hover:bg-gray-100 cursor-pointer"
        @click="goToChat(chat.id)"
      >
        {{ chat.name || "Unnamed Chat" }} (ID: {{ chat.id }})
      </li>
    </ul>
  </div>
</template>