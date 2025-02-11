<template>
  <div ref="chartContainer" class="w-full h-[300px] relative print:h-[300px]">
    <!-- Bind the passed canvasId prop if needed, or remove it if not -->
    <canvas :id="canvasId" ref="chartCanvas" class="w-full h-full"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';

// Define props. The canvasId prop is optional—if you don't need to query by ID externally,
// you can simply use the ref "chartCanvas".
const props = defineProps({
  canvasId: { type: String, default: '' },
  chartType: { type: String, default: 'bar' },
  chartData: { type: Object, required: true }
});

const chartCanvas = ref(null);
const chartInstance = ref(null);
const chartContainer = ref(null);
let resizeObserver = null;

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    }
  }
};

const initChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
  // Use the ref "chartCanvas" directly rather than looking it up by ID.
  chartInstance.value = new Chart(chartCanvas.value, {
    type: props.chartType,
    data: props.chartData,
    options: chartOptions
  });
};

watch(() => props.chartData, initChart, { deep: true });

const handleResize = () => {
  if (chartInstance.value) {
    chartInstance.value.resize();
  }
};

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

<style scoped></style>