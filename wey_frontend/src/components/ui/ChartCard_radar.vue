<template>
  <div class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 relative ">
    <div class="flex flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium">{{ title }}</span>
      <div class="w-full">
        <p class="text-sm text-gray-700 mb-4 truncate">{{ description }}</p>
      </div>

      <!-- Chart Container -->
      <div ref="chartContainer" class="chart-container relative w-full h-[300px] print:h-[300px]">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from "vue";
import { Chart, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from "chart.js";

// Register required components
Chart.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const props = defineProps({
  title: { type: String, default: "Radar Chart" },
  description: { type: String, default: "This is a radar chart." },
  labels: { type: Array, required: true },
  datasets: { type: Array, required: true }
});

const chartCanvas = ref(null);
const chartContainer = ref(null);
let chartInstance = null;
let resizeObserver = null; // Declare resizeObserver

const createChart = () => {
  if (!chartCanvas.value) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(chartCanvas.value, {
    type: "radar",
    data: {
      labels: props.labels,
      datasets: props.datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // ✅ Prevents weird stretching issues
      scales: {
        r: {
          beginAtZero: true,
          min: 0,
          max: 5,
          ticks: {
            stepSize: 1,
            font: { size: 14 },
            color: "#B0B0B0",
            backdropColor: "rgba(0,0,0,0)", // ✅ Removes background box
            padding: 5, // ✅ Ensures spacing
            showLabelBackdrop: false, // ✅ Removes default box around numbers
          },
          grid: {
            color: "rgba(200, 200, 200, 0.2)",
            circular: false // ✅ Ensures circular radar layout
          }
        }
      },
      plugins: {
        legend: {
          display: true,
          position: "top",
          labels: { color: "#FFF", font: { size: 14 } }
        }
      },
      elements: {
        line: { borderWidth: 2 },
        point: { radius: 5 }
      }
    }
  });
};

// Handle chart resize properly
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
};

const handlePrintResize = () => {
  console.log("🔄 Adjusting chart size for print...");

  if (chartInstance) {
    chartInstance.resize(); // ✅ Force chart to resize properly
  }
};

onMounted(() => {
  createChart();

  // ✅ Properly attach ResizeObserver
  resizeObserver = new ResizeObserver(handleResize);
  if (chartContainer.value) {
    resizeObserver.observe(chartContainer.value);
  }

  window.addEventListener("beforeprint", handlePrintResize);
});

// Watch for prop changes and re-render the chart
watch(() => [props.labels, props.datasets], createChart, { deep: true });

// ✅ Cleanup observer on unmount
onUnmounted(() => {
  if (resizeObserver && chartContainer.value) {
    resizeObserver.unobserve(chartContainer.value);
  }
  if (chartInstance) {
    chartInstance.destroy();
  }
  window.removeEventListener("beforeprint", handlePrintResize);
});
</script>

<style scoped>
/* ✅ Ensure Proper Sizing */
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}

canvas {
  max-width: 100%;
  height: 100% !important;
  max-height: 100%;
}
</style>