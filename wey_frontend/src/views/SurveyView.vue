<template>
  <div class="min-h-screen bg-gray-900 text-white p-6 flex flex-col items-center">
    <!-- Progress Bar -->
    <div class="w-full max-w-xl">
      <div class="h-2 bg-gray-700 rounded mb-6">
        <div :style="{ width: progressWidth + '%' }" class="h-full bg-blue-500 rounded"></div>
      </div>
    </div>

    <!-- Survey Content -->
    <div class="w-full max-w-xl bg-gray-800 p-6 rounded-lg shadow-lg">
      <!-- 현재 질문 -->
      <div>
        <h1 class="text-2xl font-bold mb-4">{{ currentQuestion.text }}</h1>
        <p v-if="currentQuestion.description" class="text-gray-400 mb-4">
          {{ currentQuestion.description }}
        </p>

        <!-- 질문 컴포넌트 -->
        <Question :question="currentQuestion" v-model="responses[currentQuestion.id]" />

        <div class="flex justify-between mt-6">
          <!-- 이전 버튼 -->
          <button @click="prevQuestion" :disabled="isFirstQuestion"
            class="px-4 py-3 rounded-lg bg-gray-700 hover:bg-gray-600 text-white disabled:opacity-50 disabled:cursor-not-allowed">
            이전
          </button>

          <!-- 다음/제출 버튼 -->
          <button v-if="!isLastQuestion" @click="nextQuestion"
            class="px-4 py-3 rounded-lg bg-blue-500 hover:bg-blue-600 text-white">
            다음
          </button>
          <button v-else @click="submitSurvey" class="px-4 py-3 rounded-lg bg-green-500 hover:bg-green-600 text-white">
            제출하기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import Question from '../components/ui/question.vue';

import PaginationControls from '../components/ui/pagninationControls.vue';

import { surveyData } from '../stores/surveyData.js';

export default {
  components: { Question },
  data() {
    return {
      surveyData, // 설문 데이터
      responses: {}, // 사용자 응답
      currentQuestionIndex: 0, // 현재 질문 인덱스
    };
  },
  computed: {
    currentQuestion() {
      // 현재 질문 반환
      return this.allQuestions[this.currentQuestionIndex];
    },
    progressWidth() {
      // 진행도를 %로 계산
      return ((this.currentQuestionIndex + 1) / this.allQuestions.length) * 100;
    },
    isFirstQuestion() {
      return this.currentQuestionIndex === 0;
    },
    isLastQuestion() {
      return this.currentQuestionIndex === this.allQuestions.length - 1;
    },
    allQuestions() {
      // 모든 질문을 순서대로 결합
      const demographicQuestions =
        this.responses.surveyType === "개인용"
          ? this.surveyData.demographics.personal
          : this.surveyData.demographics.corporate;

      return [
        // { text: "참여하고 싶은 교육 과정을 선택하세요", id: "course", type: "single", options: ["비전하우스", "리더십과 혁신 교육", "기업가정신"], },
        { id: "course", text: "참여하고 싶은 교육 과정을 선택하세요", type: "single", options: ["비전하우스", "리더십과 혁신", "기업가정신과 혁신"] },
        { text: "개인용 또는 기업용 설문을 선택하세요", id: "surveyType", type: "single", options: ["개인용", "기업용"] },
        ...demographicQuestions,
        ...this.surveyData.lifestyle,
        ...(this.surveyData.courseQuestions[this.responses.course] || []),
      ];
    },
  },
  methods: {
    nextQuestion() {
      if (!this.isLastQuestion) {
        this.currentQuestionIndex++;
      }
    },
    prevQuestion() {
      if (!this.isFirstQuestion) {
        this.currentQuestionIndex--;
      }
    },
    submitSurvey() {
      console.log("응답 데이터:", this.responses);
      console.log("All Questions:", this.allQuestions);
      alert("설문이 제출되었습니다. 감사합니다!");
    },
  },
};
</script>