<template>
  <!-- Card Container -->
  <Card style="background-color: #050818;"
    class="border border-gray-light shadow-sm rounded-lg w-full h-auto md:max-h-[440px] md:min-h-[440px] overflow-hidden ">
    <!-- Card Title -->
    <template #title>
      {{ title }}
    </template>

    <!-- Card Content -->
    <template #content>
      <!-- Description -->
      <p class="text-sm text-gray-700 mb-4">{{ description }}</p>

      <!-- Chart Container -->
      <div class="chart-container w-full h-full max-h-[250px] md:max-h-[300px]">
        <!-- Check if data is loading -->
        <div v-if="loading">Loading...</div>
        <div v-else></div>
        <Chart v-if="chartData && chartOptions" :type="chartType" :data="chartData" :options="chartOptions"
          class="h-full" />
      </div>

    </template>
  </Card>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import Card from 'primevue/card';
import Chart from 'primevue/chart';
import axios from 'axios';

// Define props
defineProps({
  title: {
    type: String,
    required: true,
    default: 'Card Title',
  },
  description: {
    type: String,
    required: false,
    default: 'This is a default description.',
  },
  chartType: {
    type: String,
    required: true,
    default: 'pie', // Default to a pie chart
  },
  chartData: {
    type: Object,
    required: false, // Optional, parent can pass data directly
    default: () => null,
  },
  chartOptions: {
    type: Object,
    required: false,
    default: () => ({}), // Allow parent to pass chart options
  },
  title_x: {
    type: String,
    required: false,
    default: 'X Axis',
  },
  title_y: {
    type: String,
    required: false,
    default: 'Y Axis',
  },
  apiUrl: {
    type: String,
    required: false, // Optional, for fetching data from an API
    default: null,
  },
});

// Reactive data and loading state
const localChartData = ref(null); // Local chart data when fetched via API
const loading = ref(true); // Loading state

// Merged chart options (combine default options with parent-provided options)
const mergedChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#ffffff', // White text for legend
      },
    },
    tooltip: {
      callbacks: {
        label: (context) => `${context.raw}명`, // Tooltip label
      },
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: title_x,
        color: '#ffffff', // White text for axis title
        font: {
          size: 14,
        },
      },
      ticks: {
        color: '#ffffff', // White text for X-axis labels
      },
    },
    y: {
      title: {
        display: true,
        text: title_y,
        color: '#ffffff', // White text for axis title
        font: {
          size: 14,
        },
      },
      ticks: {
        color: '#ffffff', // White text for Y-axis labels
      },
      beginAtZero: true,
    },
  },
  ...chartOptions, // Merge parent-provided options
}));

// Fetch data from API if `apiUrl` is provided
onMounted(async () => {
  if (!apiUrl) {
    loading.value = false; // No API URL, assume data is passed via props
    return;
  }

  try {
    const response = await axios.get(apiUrl); // Fetch data from API
    const data = response.data;

    // Transform the data into Chart.js format
    localChartData.value = {
      labels: data.labels, // Example: ['January', 'February', 'March']
      datasets: [
        {
          label: '사용자 수',
          data: data.values, // Example: [50, 120, 200]
          backgroundColor: [
            '#A78BFA', // Tailwind purple-500
            '#C4B5FD', // Tailwind purple-400
            '#DDD6FE', // Tailwind purple-300
          ],
          hoverBackgroundColor: [
            '#A78BFA', // Tailwind purple-500
            '#C4B5FD', // Tailwind purple-400
            '#DDD6FE', // Tailwind purple-300
          ],
        },
      ],
    };
  } catch (error) {
    console.error('Failed to fetch data:', error.message);
  } finally {
    loading.value = false; // Stop loading spinner
  }
});

// Use either passed-in chartData (prop) or locally fetched data
const finalChartData = computed(() => chartData || localChartData.value);
</script>