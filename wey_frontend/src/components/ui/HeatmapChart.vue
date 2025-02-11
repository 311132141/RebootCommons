<template>
  <div class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 relative">
    <div class="flex flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium">{{ title }}</span>
      <div class="w-full">
        <p class="text-sm text-gray-700 mb-4 truncate">{{ description }}</p>
      </div>
      <apexchart type="heatmap" height="300" :options="chartOptions" :series="series"></apexchart>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import VueApexCharts from "vue3-apexcharts";

// Props to pass data dynamically
const props = defineProps({
  title: { type: String, default: "Lifestyle & Course Improvement Heatmap" },
  description: { type: String, default: "This heatmap shows the relationship between lifestyle habits and course improvement." },
  lifestyleLabels: {
    type: Array,
    default: () => ["Sleep", "Exercise", "Meditation", "Diet", "Work-Life Balance"]
  },
  scores: {
    type: Array,
    default: () => [1, 2, 3, 4, 5] // Lifestyle scores
  },
  improvementData: {
    type: Array,
    default: () => [
      [1.2, 1.5, 2.1, 1.8, 1.9], // Score 1
      [2.4, 2.7, 3.0, 2.9, 2.5], // Score 2
      [3.5, 3.2, 3.8, 3.4, 3.9], // Score 3
      [4.1, 4.3, 4.7, 4.5, 4.2], // Score 4
      [5.0, 5.2, 5.5, 5.1, 5.3]  // Score 5
    ]
  }
});

// Convert data into ApexCharts series format
const series = computed(() => {
  return props.scores.map((score, index) => ({
    name: `Score ${score}`,
    data: props.lifestyleLabels.map((label, i) => ({
      x: label,
      y: props.improvementData[index][i] // Improvement Score
    }))
  }));
});

// Chart options
const chartOptions = ref({
  chart: {
    type: "heatmap",
    toolbar: { show: false }
  },
  dataLabels: {
    enabled: true,
    style: { colors: ["#fff"] } // White text inside cells
  },
  colors: ["#4F46E5"], // Change heatmap color
  xaxis: {
    categories: props.lifestyleLabels,
    labels: { style: { colors: "#ccc" } }
  },
  yaxis: {
    title: { text: "Lifestyle Score", style: { color: "#ccc" } },
    labels: { style: { colors: "#ccc" } }
  },
  tooltip: {
    enabled: true,
    theme: "dark",
    y: { formatter: (value) => `${value.toFixed(2)} Avg Improvement` }
  }
});
</script>

<style scoped>
.apexcharts-tooltip {
  background: rgba(0, 0, 0, 0.8) !important;
}
</style>