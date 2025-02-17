<template>

  <div
    class=" shadow p-4 rounded-border border border-gray-600 rounded-lg print:border-gray-500 h-full print:shadow-none">
    <div class="flex justify-between flex-col gap-2">
      <span class="block text-surface-500 dark:text-surface-300 font-medium print:text-black">{{ title }}</span>
      <h5 class=" print:text-black">{{ description }}</h5>
      <div>
        <span class="text-green-500 font-medium">{{ percentage }} </span>
        <span class="text-surface-500 dark:text-surface-300 print:text-black">{{ content }}</span>
      </div>
    </div>

  </div>


</template>

<script setup>
import { defineProps } from 'vue';
import Card from 'primevue/card';
defineProps({
  title: {
    type: String,
    required: true,
    default: '총 사용자 수',
  },
  description: {
    type: String,
    required: false,
    default: '150명',
  },
  percentage: {
    type: String,
    required: false,
    default: '26%',
  },
  content: {
    type: String,
    required: false,
    default: '증가(지난달 대비)',
  }
})
</script>