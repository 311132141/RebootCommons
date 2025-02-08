<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  question: {
    type: Object,
    default: '삶의 여유를 가지고 생활하는 편이다.'
  },
  modelValue: {
    type: [String, Array, Number],
    default: null
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
// Emit event for v-model updates
const emit = defineEmits(['update:modelValue'])

// Handle selected value for rating type questions
const selectedValue = ref(props.modelValue)

// Update function for rating-type questions
const updateValue = (value) => {
  selectedValue.value = value
  emit("update:modelValue", value)
}

// Function to toggle multiple-choice options
const toggleOption = (option) => {
  const newValue = [...(props.modelValue || [])]
  const index = newValue.indexOf(option)
  if (index === -1) {
    newValue.push(option)
  } else {
    newValue.splice(index, 1)
  }
  emit("update:modelValue", newValue)
}

// const selectedValue = ref(null)
</script>

<template v-else-if="question.type === 'rating'">
  <div class="w-full max-w-2xl mx-auto p-6">
    <div class="mb-6 text-center text-white text-lg">
      {{ question.text }}
    </div>

    <div class="flex flex-col space-y-2">
      <div class="flex justify-between items-center">
        <div class="grid grid-cols-5 gap-4 w-full mx-8">
          <template v-for="n in (question.points || 5)" :key="n">
            <div class="flex flex-col items-center">
              <button @click="updateValue(n)"
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
        <span>{{ question.labels?.left || '전혀 그렇지 않다' }}</span>
        <span>{{ question.labels?.right || '매우 그렇다' }}</span>
      </div>
    </div>
  </div>
</template>