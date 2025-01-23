<template>
  <div class="bg-gray-900 text-white p-6 rounded-lg shadow-lg">
    <!-- 질문 -->
    <h2 class="text-2xl font-bold mb-2">{{ question.text }}</h2>
    <p class="text-gray-400 mb-4">{{ question.description }}</p>

    <!-- 선택 항목 -->
    <div class="space-y-3">
      <button v-for="option in question.options" :key="option.value" @click="selectOption(option.value)" :class="[
        'w-full text-left px-4 py-3 rounded-lg font-medium transition-colors',
        selectedValue === option.value
          ? 'bg-blue-600 text-white'
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
      ]">
        <span class="block text-lg">{{ option.label }}</span>
        <span class="block text-sm text-gray-400">{{ option.description }}</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    question: {
      type: Object,
      required: true,
    },
    modelValue: {
      type: String,
      default: null,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      selectedValue: this.modelValue,
    };
  },
  methods: {
    selectOption(value) {
      this.selectedValue = value;
      this.$emit("update:modelValue", value); // 부모로 선택값 전달
    },
  },
};
</script>

<style scoped>
/* 버튼 hover와 transition 스타일을 Tailwind와 함께 확장 가능 */
</style>