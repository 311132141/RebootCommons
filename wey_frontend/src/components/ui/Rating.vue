<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  question: {
    type: Object,
    default: () => ({ text: '삶의 여유를 가지고 생활하는 편이다.', type: 'rating' })
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
// Include "answered" in the emits list.
const emit = defineEmits(['update:modelValue', 'answered'])

// Handle selected value for rating-type questions
const selectedValue = ref(props.modelValue)
const updateValue = (value) => {
  selectedValue.value = value
  emit("update:modelValue", value)
  // Emit "answered" so the parent can trigger the auto-scroll.
  emit("answered")
}
</script>

<template v-else-if="question.type === 'rating'">
  <div class="w-full max-w-4xl mx-auto mt-6 pt-6 transition-all duration-300" :class="{
    'opacity-100 text-white': question.id === activeQuestionId
  }">
    <div class="mb-6 text-center text-white md:mb-12">
      <h6 class="break-keep text-base md:text-lg">{{ question.text }}</h6>

    </div>

    <!-- Responsive Wrapper -->
    <!-- <div class="flex flex-col space-y-2"> -->
    <!-- Rating Row -->
    <div class="flex justify-between items-center flex-row md:mx-12">
      <!-- flex flex-col items-center space-y-4 -->
      <!-- Left Label -->
      <span class="whitespace-nowrap text-center hidden md:flex">
        {{ question.labels?.left || '전혀 그렇지 않다' }}
      </span>
      <!-- Rating Buttons -->
      <div class="grid grid-cols-5 gap-4 w-full  md:mx-4">
        <template v-for="n in (question.points || 5)" :key="n">
          <div class="flex flex-col  items-center">
            <button @click="updateValue(n)"
              class="w-12 h-12 rounded-full border-2 transition-all duration-200 focus:outline-none md:w-14 md:h-14 items-center justify-center place-items-center"
              :class="[
                selectedValue === n
                  ? 'border-purple-500 bg-purple-500'
                  : 'border-gray-400 bg-transparent hover:border-purple-300'
              ]">
              <span class="sr-only">Option {{ n }}</span>
              <!-- Tick Icon (Only visible when selected) -->
              <svg v-if="selectedValue === n" xmlns="http://www.w3.org/2000/svg"
                class="md:w-10 md:h-10 w-8 h-8 items-center justify-center" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </button>
          </div>
        </template>

      </div>
      <!-- Right Label -->
      <span class="whitespace-nowrap text-center hidden md:flex ">
        {{ question.labels?.right || '매우 그렇다' }}
      </span>

    </div>
    <div class="flex justify-between text-gray-400 md:hidden pt-3">
      <span>{{ question.labels?.left || '전혀 그렇지 않다' }}</span>
      <span>{{ question.labels?.right || '매우 그렇다' }}</span>
    </div>
    <hr class="border-t border-gray-100 mt-8 opacity-50 md:mt-16">

  </div>

  <!-- </div> -->
</template>