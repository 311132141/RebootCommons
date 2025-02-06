<template>
  <div ref="chartContainer" class="w-full h-[300px] md:h-[400px] relative">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';

// Define props
const props = defineProps({
  title: { type: String, default: 'Chart Title' },
  description: { type: String, default: 'This is a chart.' },
  chartType: { type: String, default: 'bar' },  // Pie chart can be passed dynamically
  chartData: { type: Object, required: true },
});

// Refs
const chartCanvas = ref(null);
const chartInstance = ref(null);
const chartContainer = ref(null);
let resizeObserver = null;

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#ffffff',
      },
    },
    tooltip: {
      callbacks: {
        label: (context) => `${context.raw}명`,
      },
    },
  },
};

// Function to initialize chart
const initChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }

  chartInstance.value = new Chart(chartCanvas.value, {
    type: props.chartType,  // Dynamically set type (bar, pie, etc.)
    data: props.chartData,
    options: chartOptions,
  });
};

// Watch for data changes and update the chart
watch(() => props.chartData, initChart, { deep: true });

// Handle resizing
const handleResize = () => {
  if (chartInstance.value) {
    chartInstance.value.resize();
  }
};

// Lifecycle Hooks
onMounted(() => {
  initChart();
  resizeObserver = new ResizeObserver(handleResize);
  if (chartContainer.value) {
    resizeObserver.observe(chartContainer.value);
  }
});

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style>