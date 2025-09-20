<script setup lang="ts">
import { Line } from "vue-chartjs"
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from "chart.js"
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale)

const route = useRoute()
const config = useRuntimeConfig()

// Fetch time series stats
const { data: timeSeries } = await useFetch(
  `${config.public.apiBase}/api/stats/${route.params.id}/time_series?interval=month`
)

// Fetch summary stats
const { data: summary } = await useFetch(
  `${config.public.apiBase}/api/stats/${route.params.id}/summary`
)

const chartData = {
  labels: timeSeries.value?.labels || [],
  datasets: [
    {
      label: "Messages",
      data: timeSeries.value?.counts || [],
      borderColor: "rgb(75, 192, 192)",
      fill: false,
    },
  ],
}
</script>

<template>
  <div class="p-6">
    <h1 class="text-xl font-bold mb-4">Chat {{ route.params.id }}</h1>

    <!-- Chart -->
    <Line :data="chartData" />

    <!-- Summary Stats -->
    <div v-if="summary" class="mt-6 space-y-2">
      <p><strong>Total Messages:</strong> {{ summary.total_messages }}</p>
      <p><strong>Participants:</strong> {{ summary.num_participants }}</p>

      <div>
        <h2 class="text-lg font-semibold">Top Senders</h2>
        <ul class="list-disc list-inside">
          <li v-for="sender in summary.top_senders" :key="sender.sender">
            {{ sender.sender }} - {{ sender.count }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
