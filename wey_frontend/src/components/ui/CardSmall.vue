<template>
  <!-- Card Container -->
  <Card style="background-color: #050818;"
    class="border border-gray-light shadow-sm rounded-lg w-full h-auto md:max-h-[440px] overflow-hidden ">
    <!-- Card Title -->
    <template #title>
      <h2 class="text-lg font-light">{{ title }}</h2>
    </template>

    <!-- Card Content -->
    <template #subtitle>
      <!-- Description -->
      <div class="text-3xl font-semibold mb-2 text-white">{{ description }}</div>


      <div class="flex items-center space-x-2">
        <!-- Percentage Badge -->
        <span class="px-2 py-1 rounded-full bg-green-900 text-green-400 text-sm font-medium">{{ percentage }} </span>

        <!-- Description -->
        <span class="text-gray-400 text-sm">{{ content }}</span>
      </div>


    </template>
  </Card>
</template>

<script setup>
import { defineProps } from 'vue';
import Card from 'primevue/card';
defineProps({
  title: {
    type: String,
    required: true,
    default: 'Card Title',
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