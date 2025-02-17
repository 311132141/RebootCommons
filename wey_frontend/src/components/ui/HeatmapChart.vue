<template>
  <div class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 relative">
    <div class="flex flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium print:text-black">
        {{ title }}
      </span>
      <div class="w-full">
        <p class="text-sm text-gray-400 mb-4 truncate">{{ description }}</p>
      </div>
      <!-- Chart Container with ref -->
      <apexchart ref="apexchartRef" type="heatmap" height="300" :options="chartOptions" :series="series">
      </apexchart>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import VueApexCharts from "vue3-apexcharts"; // Ensure you've registered/use this component

// Define props
const props = defineProps({
  title: { type: String, default: "Lifestyle & Course Improvement Heatmap" },
  description: { type: String, default: "This heatmap shows the relationship between lifestyle habits and course improvement." },
  lifestyleLabels: {
    type: Array,
    default: () => ["Sleep", "Exercise", "Meditation", "Diet", "Work-Life Balance"]
  },
  scores: {
    type: Array,
    default: () => [1, 2, 3, 4, 5]
  },
  improvementData: {
    type: Array,
    default: () => [
      [1.2, 1.5, 2.1, 1.8, 1.9],
      [2.4, 2.7, 3.0, 2.9, 2.5],
      [3.5, 3.2, 3.8, 3.4, 3.9],
      [4.1, 4.3, 4.7, 4.5, 4.2],
      [5.0, 5.2, 5.5, 5.1, 5.3]
    ]
  }
});

// Convert data into ApexCharts series format
const series = computed(() => {
  return props.scores.map((score, index) => ({
    name: `Score ${score}`,
    data: props.lifestyleLabels.map((label, i) => ({
      x: label,
      y: props.improvementData[index][i]
    }))
  }));
});

// Chart options (default on-screen settings)
const chartOptions = ref({
  chart: {
    type: "heatmap",
    toolbar: { show: false }
  },
  dataLabels: {
    enabled: true,
    style: { colors: ["#fff"] } // White text inside cells
  },
  colors: ["#4F46E5"], // Default heatmap color
  xaxis: {
    categories: props.lifestyleLabels,
    labels: { style: { colors: "#ccc" } } // Default x-axis label color
  },
  yaxis: {
    title: { text: "Lifestyle Score", style: { color: "#ccc" } },
    labels: { style: { colors: "#ccc" } } // Default y-axis label color
  },
  tooltip: {
    enabled: true,
    theme: "dark",
    y: { formatter: (value) => `${value.toFixed(2)} Avg Improvement` }
  }
});

// Reference to the ApexCharts component
const apexchartRef = ref(null);

// Define print mode functions
function handleCustomBeforePrint() {
  if (apexchartRef.value) {
    // Update options for print mode:
    apexchartRef.value.updateOptions({
      xaxis: {
        labels: { style: { colors: "#000000" } } // Black x-axis labels
      },
      yaxis: {
        labels: { style: { colors: "#000000" } },  // Black y-axis labels
        title: { style: { color: "#000000" } }      // Black y-axis title
      },
      tooltip: {
        theme: "light" // Switch tooltip to light theme if desired
      },
      colors: ["#000000"] // Change heatmap color to black (or any print-friendly color)
    });
    console.log("Print mode options applied for ApexCharts.");
  }
}

function handleCustomAfterPrint() {
  if (apexchartRef.value) {
    // Revert options back to original on-screen settings:
    apexchartRef.value.updateOptions({
      xaxis: {
        labels: { style: { colors: "#ccc" } }
      },
      yaxis: {
        labels: { style: { colors: "#ccc" } },
        title: { style: { color: "#ccc" } }
      },
      tooltip: {
        theme: "dark"
      },
      colors: ["#4F46E5"]
    });
    console.log("Default chart options restored after print.");
  }
}

// Add event listeners for printing
onMounted(() => {
  window.addEventListener("beforeprint", handleCustomBeforePrint);
  window.addEventListener("afterprint", handleCustomAfterPrint);
});

onUnmounted(() => {
  window.removeEventListener("beforeprint", handleCustomBeforePrint);
  window.removeEventListener("afterprint", handleCustomAfterPrint);
});
</script>