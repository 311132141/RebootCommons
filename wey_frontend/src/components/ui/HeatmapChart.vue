<template>
  <div>
    <ApexChart type="heatmap" :options="chartOptions" :series="chartSeries" class="w-full" />
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Function to generate random data
const generateData = (count, range) => {
  const data = [];
  for (let i = 0; i < count; i++) {
    data.push({
      x: `W${i + 1}`, // Example labels (W1, W2, etc.)
      y: Math.floor(Math.random() * (range.max - range.min + 1)) + range.min, // Random value between min and max
    });
  }
  return data;
};

// Chart series data
const chartSeries = [
  {
    name: 'Metric1',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric2',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric3',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric4',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric5',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric6',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric7',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric8',
    data: generateData(18, { min: 0, max: 90 }),
  },
  {
    name: 'Metric9',
    data: generateData(18, { min: 0, max: 90 }),
  },
];

// Chart configuration options
const chartOptions = {
  chart: {
    height: 350,
    type: 'heatmap',
  },
  dataLabels: {
    enabled: false,
  },
  colors: ['#008FFB'], // Single color
  title: {
    text: 'HeatMap Chart (Single Color)',
  },
};
</script>

<style scoped>
/* Optional styles */
</style>