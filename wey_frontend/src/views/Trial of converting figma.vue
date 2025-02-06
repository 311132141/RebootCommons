<template>
  <div class="min-h-screen flex flex-col bg-gray-900 text-white px-6">
    <!-- Progress Bar & Header -->
    <div class="w-full flex flex-col items-center gap-[1.625rem] pt-14">
      <!-- Mobile Header -->
      <div class="flex justify-between items-center self-stretch md:hidden" data-layer="Header">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        <h6>인구통계학</h6>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>
      </div>

      <!-- Progress bar -->
      <div class="w-full">
        <div class="h-2 bg-gray-700 rounded">
          <div :style="{ width: progressWidth + '%' }" class="h-full bg-purple-500 rounded"></div>
        </div>
      </div>


      <!-- Desktop Header -->
      <div class="justify-between items-center self-stretch hidden md:inline-flex" data-layer="second_header">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        <h6>인구통계학</h6>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>
      </div>

      <!-- Current question header (mobile only) -->
      <div class="w-full md:hidden">
        <div class="Question h-10 text-white text-xl font-medium font-['Gmarket Sans TTF'] leading-normal text-left"
          data-layer="question">
          {{ currentQuestion.text }}
        </div>
      </div>
    </div>

    <!-- Question Content -->
    <!-- The Question component expects:
         :question="currentQuestion"
         v-model="responses[currentQuestion.id]"
         You must ensure @/components/ui/question.vue is set up
         to accept those props properly -->
    <Question v-if="questions.length > 0" :question="currentQuestion" v-model="responses[currentQuestion.id]"
      class="sm:mt-auto md:mt-0 overflow-hidden" />

    <!-- Navigation Buttons -->
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
import Question from "@/components/ui/question.vue"; // Adjust path if needed

export default {
  name: "SurveyPage",
  components: {
    Question,
  },
  data() {
    return {
      // We'll store the question data from the API here
      questions: [],
      // The user's answers, keyed by question ID
      responses: {},
      // Current question index for navigation
      currentQuestionIndex: 0,

      // Example: you might get these from a previous step, Vuex store, etc.
      surveyTypeId: 1,
      courseTypeId: 1,

      // Phase can be 'pre' or 'post'. Hard-coded or user-chosen:
      selectedPhase: "pre",
    };
  },
  computed: {
    // Return the current question object
    currentQuestion() {
      return this.questions[this.currentQuestionIndex] || {};
    },
    // Calculation for the progress bar
    progressWidth() {
      if (this.questions.length === 0) return 0;
      return (
        ((this.currentQuestionIndex + 1) / this.questions.length) * 100
      );
    },
    // Are we on the first question?
    isFirstQuestion() {
      return this.currentQuestionIndex === 0;
    },
    // Are we on the last question?
    isLastQuestion() {
      return this.currentQuestionIndex === this.questions.length - 1;
    },
  },
  mounted() {
    // When this component mounts, fetch the questions from the API
    this.fetchQuestions();
  },
  methods: {
    // Make GET request to your Django endpoint
    async fetchQuestions() {
      try {
        // Adjust the URL if needed
        const url = `http://127.0.0.1:8000/api/survey/${this.surveyTypeId}/${this.courseTypeId}/`;

        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // If your endpoint requires auth, add it here
            // "Authorization": `Bearer ${someToken}`,
          },
        });

        if (!response.ok) {
          console.error("Failed to fetch questions, status:", response.status);
          return;
        }

        // Store the questions
        this.questions = await response.json();
        console.log("Fetched questions:", this.questions);
        console.log("Checking if it works:", this.questions[0].text);


        // Reset the responses map
        this.responses = {};

        // Reset index to the start
        this.currentQuestionIndex = 0;
      } catch (err) {
        console.error("Error fetching questions:", err);
      }
    },

    // Move forward in the question array
    nextQuestion() {
      if (!this.isLastQuestion) {
        this.currentQuestionIndex++;
      }
    },
    // Move backward in the question array
    prevQuestion() {
      if (!this.isFirstQuestion) {
        this.currentQuestionIndex--;
      }
    },

    // Submit the entire survey
    async submitSurvey() {
      try {
        // Turn responses object into an array matching your backend's expectation
        // e.g. { "14": "남성", "15": "대학졸업" } -> [ { question_id: 14, answer_text: "남성" }, ... ]
        const answersArray = Object.entries(this.responses).map(
          ([questionId, answerVal]) => {
            return {
              question_id: parseInt(questionId),
              // Decide logic for text vs. rating, etc.
              answer_text: typeof answerVal === "string" ? answerVal : null,
              answer_value: typeof answerVal === "number" ? answerVal : null,
            };
          }
        );

        const bodyData = {
          phase: this.selectedPhase, // 'pre' or 'post'
          answers: answersArray,
        };

        const url = `http://127.0.0.1:8000/api/survey/${this.surveyTypeId}/${this.courseTypeId}/`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // "Authorization": `Bearer ${someToken}`,
          },
          body: JSON.stringify(bodyData),
        });

        const result = await response.json();
        if (response.ok) {
          console.log("Survey submitted successfully:", result);
          alert("설문이 제출되었습니다. 감사합니다!");
        } else {
          console.error("Survey submission failed:", result);
          alert("설문 제출에 실패했습니다.");
        }
      } catch (err) {
        console.error("Error submitting survey:", err);
      }
    },
  },
};
</script>

<style scoped>
/* Keep or modify your existing styles. */
.size-6 {
  width: 24px;
  height: 24px;
}
</style>
