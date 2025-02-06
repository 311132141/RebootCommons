<script setup>
import { ref } from 'vue'

const props = defineProps({
  question: {
    type: String,
    default: '삶의 여유를 가지고 생활하는 편이다.'
  },
  labels: {
    type: Object,
    default: () => ({
      left: '전혀 그렇지 않다',
      right: '매우 그렇다'
    })
  },
  points: {
    type: Number,
    default: 5
  }
})

const selectedValue = ref(null)
</script>

<template>
  <div class="w-full max-w-2xl mx-auto p-6">
    <div class="mb-6 text-center text-white text-lg">
      {{ question }}
    </div>

    <div class="flex flex-col space-y-2">
      <div class="flex justify-between items-center">
        <div class="grid grid-cols-5 gap-4 w-full mx-8">
          <template v-for="n in points" :key="n">
            <div class="flex flex-col items-center">
              <button @click="selectedValue = n"
                class="w-12 h-12 rounded-full border-2 transition-all duration-200 focus:outline-none" :class="[
                  selectedValue === n
                    ? 'border-blue-500 bg-blue-500'
                    : 'border-gray-400 bg-transparent hover:border-blue-300'
                ]">
                <span class="sr-only">Option {{ n }}</span>
              </button>
            </div>
          </template>
        </div>
      </div>

      <div class="flex justify-between text-gray-400 px-4">
        <span>{{ labels.left }}</span>
        <span>{{ labels.right }}</span>
      </div>
    </div>
  </div>
</template>