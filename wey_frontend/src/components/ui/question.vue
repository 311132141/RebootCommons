<template>
  <div class="mb-6">
    <!-- 질문 제목 -->
    <!-- <label class="block font-bold text-lg mb-4">{{ question.text }}</label> -->

    <!-- Text Input -->
    <template v-if="question.type === 'text'">
      <input type="text" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"
        class="w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
    </template>

    <!-- Single Choice -->
    <template v-else-if="question.type === 'single'">
      <div class=" w-full flex justify-center pb-9 flex-col items-center gap-2 md:hidden">
        <button v-for="option in question.options" :key="option" @click="$emit('update:modelValue', option)" :class="[
          'w-full py-4 rounded-2xl transition-colors',
          modelValue === option
            ? 'bg-blue-500 text-white'
            : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
        ]">
          <b2>{{ option }}</b2>
        </button>
      </div>
      <div class=" hidden md:flex items-center justify-center min-h-[calc(100vh_-_13vh)]">
        <div data-layer="Frame 660"
          class=" w-[30rem] lg:w-[36rem] flex-col justify-start items-center gap-14 inline-flex">
          <div data-layer="Group 26" class="flex-col items-center justify-center gap-4 inline-flex">
            <b2>귀하의 성별은?</b2>
            <h4 class="font-bold">인구통계학</h4>

          </div>
          <div class=" w-full flex justify-center pb-9 flex-col items-center gap-2 ">
            <button v-for="option in question.options" :key="option" @click="$emit('update:modelValue', option)" :class="[
              'w-full py-[1.25rem] rounded-2xl transition-colors',
              modelValue === option
                ? 'bg-blue-500 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            ]">
              <b2>{{ option }}</b2>
            </button>
          </div>
        </div>
      </div>


    </template>

    <!-- Multiple Choice -->
    <template v-else-if="question.type === 'multiple'">
      <div class="space-y-3">
        <button v-for="option in question.options" :key="option" @click="toggleOption(option)" :class="[
          'w-full text-left px-4 py-3 rounded-lg font-medium transition-colors',
          modelValue.includes(option)
            ? 'bg-blue-500 text-white'
            : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
        ]">
          {{ option }}
        </button>
      </div>
    </template>
    <!-- Likert Scale -->
    <template v-else-if="question.type === 'likert'">
      <div class="flex justify-between items-center">
        <!-- Labels -->
        <span class="text-green-500 font-medium">Agree</span>
        <div class="flex space-x-4">
          <button v-for="(option, index) in question.options" :key="index" @click="$emit('update:modelValue', option)"
            :class="[
              'w-10 h-10 flex items-center justify-center rounded-full border transition-colors',
              modelValue === option
                ? 'bg-blue-500 text-white border-blue-500'
                : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-gray-700',
            ]">
            <span class="text-sm font-medium">{{ index + 1 }}</span>
          </button>
        </div>
        <span class="text-purple-500 font-medium">Disagree</span>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    question: Object,
    modelValue: {
      type: [String, Array],
      default: null,
    },
  },
  emits: ["update:modelValue"], // Declare the emitted event
  methods: {
    toggleOption(option) {
      // 다중 선택 값 업데이트
      const newValue = [...(this.modelValue || [])];
      const index = newValue.indexOf(option);
      if (index === -1) {
        newValue.push(option); // 선택 추가
      } else {
        newValue.splice(index, 1); // 선택 제거
      }
      this.$emit("update:modelValue", newValue);
    },
  },
};
</script>