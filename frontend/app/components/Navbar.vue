<script setup lang="ts">
import ChatSearch from "./ChatSearch.vue"
import { useRouter } from "vue-router"

const router = useRouter()
</script>

<template>
  <nav class="flex items-center justify-between px-6 py-3 bg-gray-800 text-white">
    <!-- Left: Home link -->
    <div
      class="font-bold text-lg cursor-pointer hover:text-gray-300"
      @click="router.push('/')"
    >
      TeleStats
    </div>

    <!-- Right: Chat Search -->
    <div class="w-1/3">
      <ChatSearch />
    </div>
  </nav>
</template>
