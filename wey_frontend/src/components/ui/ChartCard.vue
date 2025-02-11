<template>
  <div class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 relative">
    <div class="flex flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium">{{ title }}</span>
      <div class="w-full">
        <p class="text-sm text-gray-700 mb-4 truncate">{{ description }}</p>
      </div>


      <!-- Use the ChartComponent -->
      <ReusableChart :canvasId="uniqueCanvasId" :chartType="chartType" :chartData="computedChartData" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import ReusableChart from './ReusableChart.vue';

const props = defineProps({
  title: { type: String, default: "성별 분포 (Gender Distribution)" },
  description: { type: String, default: "이 그래프는 참가자의 성별 분포를 보여줍니다." },
  chartType: { type: String, default: "pie" },
  labels: { type: Array, default: () => ["남성 (Male)", "여성 (Female)"] },
  datasets: {
    type: Array,
    default: () => [
      {
        label: "Gender Ratio",
        data: [60, 40], // Example: 60% Male, 40% Female
        backgroundColor: ["#4F46E5", "#A78BFA"]
      }
    ]
  },
  // Optional: a unique canvas id for this instance (if needed)
  canvasId: { type: String, default: '' }
});

const uniqueCanvasId = computed(() => {
  // If you provided a canvasId prop, use it; otherwise generate one (for example, using title)
  return props.canvasId || props.title.replace(/\s+/g, '-') + '-chart';
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