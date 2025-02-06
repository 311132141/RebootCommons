<template>
  <div class="min-h-screen flex flex-col bg-gray-900 text-white px-6  ">
    <!-- Progress Bar -->
    <div class="w-full  flex flex-col items-center gap-[1.625rem] pt-14">

      <div data-layer="Header" className="flex justify-between items-center self-stretch md:hidden">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        <!-- <div data-layer="인구통계학"
          className="w-80 text-center text-white text-xl font-medium font-['Gmarket Sans TTF'] leading-normal">인구통계학
        </div> -->
        <h6>인구통계학</h6>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>
      </div>
      <div class="w-full ">
        <div class="h-2 bg-gray-700 rounded ">
          <div :style="{ width: progressWidth + '%' }" class="h-full bg-purple-500 rounded"></div>
        </div>
      </div>
      <div data-layer="second_header" className="justify-between items-center  self-stretch hidden md:inline-flex">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        <!-- <div data-layer="인구통계학"
          className="w-80 text-center text-white text-xl font-medium font-['Gmarket Sans TTF'] leading-normal">인구통계학
        </div> -->
        <h6>인구통계학</h6>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>
      </div>

      <div class="w-full md:hidden">
        <div data-layer="question"
          class="Question h-10 text-white text-xl font-medium font-['Gmarket Sans TTF'] leading-normal text-left">{{
            currentQuestion.text }}
        </div>
      </div>

    </div>

    <!-- Survey Content -->
    <!-- <Likert /> -->

    <Question :question="currentQuestion" v-model="responses[currentQuestion.id]"
      class="sm:mt-auto md:mt-0 overflow-hidden" />
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
</template>
<script>

import Question from '../components/ui/question.vue';
import Likert from '../components/ui/Likert.vue';
import PaginationControls from '../components/ui/pagninationControls.vue';

import { surveyData } from '../stores/surveyData.js';
import { ChevronLeftIcon } from "@vue-hero-icons/outline"
import { ChevronRightIcon } from "@vue-hero-icons/outline"
import CardSmall from '../components/ui/CardSmall.vue';




export default {
  components: {
    Question,
    Likert
  },
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