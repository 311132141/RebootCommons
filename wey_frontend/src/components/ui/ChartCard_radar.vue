<template>
  <div class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 relative">
    <div class="flex flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium print:text-black">
        {{ title }}
      </span>
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
import { ref, onMounted, watch, onUnmounted, computed } from "vue";
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
let resizeObserver = null;

// ADDED CODE: Compute maximum value from all dataset values (with padding)
const computedMaxValue = computed(() => {
  let maxVal = 0;
  for (const ds of props.datasets) {
    if (ds.data && ds.data.length > 0) {
      const currentMax = Math.max(...ds.data);
      if (currentMax > maxVal) {
        maxVal = currentMax;
      }
    }
  }
  // Multiply by 1.1 for padding and round up; default to 5 if no data.
  return Math.ceil(maxVal * 1.1) || 5;
});

const createChart = () => {
  if (!chartCanvas.value) return;

  if (chartInstance) {
    chartInstance.destroy();
  }
  const adjustedDatasets = props.datasets.map((ds) => ({
    ...ds,
    data: ds.data.map((value) => (value < 0 ? 0 : value))
  }));

  chartInstance = new Chart(chartCanvas.value, {
    type: "radar",
    data: {
      labels: props.labels,
      datasets: adjustedDatasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          beginAtZero: true,
          min: 0,
          // CHANGED CODE: Use computed max value from the data
          max: computedMaxValue.value,
          ticks: {
            stepSize: Math.max(1, computedMaxValue.value / 5),
            font: { size: 14 },
            color: "#B0B0B0",
            backdropColor: "rgba(0,0,0,0)",
            padding: 5,
            showLabelBackdrop: false,
          },
          grid: {
            color: "rgba(200, 200, 200, 0.2)",
            circular: false
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

const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
};

const handlePrintResize = () => {
  console.log("🔄 Adjusting chart size for print...");
  if (chartInstance) {
    chartInstance.resize();
  }
};

onMounted(() => {
  createChart();

  // Attach ResizeObserver to the container
  resizeObserver = new ResizeObserver(handleResize);
  if (chartContainer.value) {
    resizeObserver.observe(chartContainer.value);
  }
  window.addEventListener("beforeprint", handlePrintResize);
});

// Watch for changes in props and re-create the chart
watch(() => [props.labels, props.datasets], createChart, { deep: true });

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