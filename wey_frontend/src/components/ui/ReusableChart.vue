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
      position: 'top',
      labels: {
        color: "#FFF", // ← Change this to the desired text color
        font: { size: 14 }
      }
    }
  },
  // If you want to change axis label colors, define your scales here (for bar/line charts):
  scales: {
    x: {
      ticks: {
        color: '#B0B0B0', // default label color
      },
      grid: {
        color: 'rgba(200,200,200,0.2)', // default grid color
      }
    },
    y: {
      ticks: {
        color: '#B0B0B0',
      },
      grid: {
        color: 'rgba(200,200,200,0.2)',
      }
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
const handleCustomBeforePrint = () => {
  if (chartInstance.value) {
    console.log("Niggaaa")
    // Change legend labels
    chartInstance.value.options.plugins.legend.labels.color = "#000000"; // black

    chartInstance.value.options.scales.x.ticks.color = '#000000';  // black
    chartInstance.value.options.scales.x.grid.color = 'rgba(0,0,0,0.2)';

    // For y-axis labels
    chartInstance.value.options.scales.y.ticks.color = '#000000';
    chartInstance.value.options.scales.y.grid.color = 'rgba(0,0,0,0.2)';

    // For legend labels
    if (chartInstance.value.options.plugins.legend.labels) {
      chartInstance.value.options.plugins.legend.labels.color = '#000000';
    }

    // If you want to update dataset colors for printing:
    chartInstance.value.data.datasets.forEach(ds => {
      // Save original if not saved
      if (!ds._defaultBackground) ds._defaultBackground = ds.backgroundColor;
      if (!ds._defaultBorder) ds._defaultBorder = ds.borderColor;

      // Example: set them to print-friendly colors
      ds.backgroundColor = 'rgba(255,0,0,0.2)';
      ds.borderColor = 'rgba(255,0,0,1)';
    })

    chartInstance.update();
  }
};

const handleCustomAfterPrint = () => {
  if (chartInstance.value) {
    // Revert x-axis
    chartInstance.value.options.scales.x.ticks.color = '#FFFFFF';
    chartInstance.value.options.scales.x.grid.color = 'rgba(200,200,200,0.2)';

    // Revert y-axis
    chartInstance.value.options.scales.y.ticks.color = '#B0B0B0';
    chartInstance.value.options.scales.y.grid.color = 'rgba(200,200,200,0.2)';

    // Revert legend
    if (chartInstance.value.options.plugins.legend.labels) {
      chartInstance.value.options.plugins.legend.labels.color = '#B0B0B0';
    }

    // Revert dataset colors
    chartInstance.value.data.datasets.forEach(ds => {
      if (ds._defaultBackground) {
        ds.backgroundColor = ds._defaultBackground;
      }
      if (ds._defaultBorder) {
        ds.borderColor = ds._defaultBorder;
      }
    });
    chartInstance.value.update();
  }
};
onMounted(() => {
  initChart();
  resizeObserver = new ResizeObserver(handleResize);
  if (chartContainer.value) {
    resizeObserver.observe(chartContainer.value);
  }
  window.addEventListener("chartBeforePrint", handleCustomBeforePrint);
  window.addEventListener("chartAfterPrint", handleCustomAfterPrint);
  // window.addEventListener("beforeprint", handleBeforePrint);
  // window.addEventListener("afterprint", handleAfterPrint);
  // window.addEventListener("chartBeforePrint", handlePrintResize);
});

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
  window.removeEventListener("chartBeforePrint", handleCustomBeforePrint);
  window.removeEventListener("chartAfterPrint", handleCustomAfterPrint);
});


</script>

<style scoped></style>