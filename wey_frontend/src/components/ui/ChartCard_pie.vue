<template>
  <div class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 relative">
    <div class="flex flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium">{{ title }}</span>
      <div class="w-full">
        <p class="text-sm text-gray-700 mb-4 truncate">{{ description }}</p>
      </div>


      <!-- Use the ChartComponent -->
      <ReusableChart title="User Growth" description="Monthly active users over time" :chartType="'pie'" :chartData="{
        labels: labels,
        datasets: [{
          label: label_name,
          data: data,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        }]
      }" :title_x="title_z" :title_y="title_y" />
    </div>
  </div>
</template>

<script setup>
import ReusableChart from './ReusableChart.vue';

// Define props
defineProps({
  title: { type: String, default: 'Chart Title' },
  description: { type: String, default: 'This is a chart.' },
  label_name: { type: String, default: 'User' },
  labels: { type: Array, default: () => ['Jan', 'Feb', 'Mar', 'Apr', 'May'] },
  data: { type: Array, default: () => [100, 200, 300, 400, 500] },
  title_z: { type: String, default: 'Month' },
  title_y: { type: String, default: 'User Count' },


});
</script>