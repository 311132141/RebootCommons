<template>
  <!-- Likert Questions -->
  <div class="flex flex-col gap-6 mt-6">
    <div v-for="(question, index) in likertQuestions" :key="question.id" class="flex flex-col items-center"
      :class="{ 'opacity-100': index === currentLikertIndex, 'opacity-50': index !== currentLikertIndex }">
      <!-- Question Text -->
      <p class="text-lg font-medium"
        :class="{ 'text-white': index === currentLikertIndex, 'text-gray-400': index !== currentLikertIndex }">
        {{ question.text }}
      </p>

      <!-- Likert Options -->
      <div class="flex justify-center gap-4 mt-4">
        <button v-for="option in question.options" :key="option" @click="selectOption(index, option)"
          class="w-12 h-12 flex items-center justify-center rounded-full border transition-colors" :class="[
            selectedAnswers[question.id] === option
              ? 'bg-blue-500 text-white border-blue-500'
              : 'bg-gray-700 text-gray-400 border-gray-600 hover:bg-gray-600',
          ]">
          {{ option }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentLikertIndex: 0, // Track the active question index
      selectedAnswers: {}, // Store selected answers keyed by question ID
      likertQuestions: [
        { id: 1, text: "삶의 여유를 가지고 생활하는 편이다.", options: ["1", "2", "3", "4", "5"] },
        { id: 2, text: "스스로를 행복한 사람이라고 생각한다.", options: ["1", "2", "3", "4", "5"] },
        { id: 3, text: "주변 사람들과 원활히 소통한다.", options: ["1", "2", "3", "4", "5"] },
        { id: 4, text: "매일 규칙적인 생활을 한다.", options: ["1", "2", "3", "4", "5"] },
      ],
    };
  },
  computed: {
    progressWidth() {
      // Calculate progress based on the number of answered questions
      const answeredCount = Object.keys(this.selectedAnswers).length;
      return (answeredCount / this.likertQuestions.length) * 100;
    },
  },
  methods: {
    selectOption(index, option) {
      const question = this.likertQuestions[index];
      this.$set(this.selectedAnswers, question.id, option); // Record the answer

      // Move to the next question if available
      if (index < this.likertQuestions.length - 1) {
        this.currentLikertIndex = index + 1;
      }
    },
    prevLikertQuestion() {
      if (this.currentLikertIndex > 0) {
        this.currentLikertIndex--;
      }
    },
    nextLikertQuestion() {
      if (this.currentLikertIndex < this.likertQuestions.length - 1) {
        this.currentLikertIndex++;
      }
    },
  },
};
</script>