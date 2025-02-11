<template>
  <div class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 relative print:h-[400px]">
    <div class="flex flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium">{{ title }}</span>
      <div class="w-full">
        <p class="text-sm text-gray-700 mb-4 truncate">{{ description }}</p>
      </div>

      <!-- Chart Component -->
      <ReusableChart :title="title" :description="description" :chartType="'bar'" :chartData="computedChartData"
        :title_x="title_z" :title_y="title_y" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import ReusableChart from "./ReusableChart.vue";

// Define props
const props = defineProps({
  title: { type: String, default: "Chart Title" },
  description: { type: String, default: "This is a chart." },
  labels: { type: Array, default: () => ["Jan", "Feb", "Mar"] },
  datasets: {
    type: Array,
    default: () => [
      { label: "남성 (Male)", data: [2.5, 3.2, 4.1], backgroundColor: "#4F46E5" },
      { label: "여성 (Female)", data: [3.4, 2.7, 3.1], backgroundColor: "#A78BFA" }
    ]
  },
  title_z: { type: String, default: "X Axis Title" },
  title_y: { type: String, default: "Y Axis Title" }
});

// Ensure computed reactivity for Chart.js data
const computedChartData = computed(() => ({
  labels: props.labels,
  datasets: props.datasets.map(dataset => ({
    ...dataset,
    data: [...dataset.data], // Unwrap Proxy if necessary
    borderColor: dataset.borderColor || "rgba(75, 192, 192, 1)",
    borderWidth: dataset.borderWidth || 1
  }))
}));
</script>