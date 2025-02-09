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
        <h6>{{ currentPageTitle }}</h6>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>
      </div>

      <!-- Progress Bar -->
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
        <h6>{{ currentPageTitle }}</h6>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>
      </div>
    </div>

    <!-- Page Content -->
    <div class="flex-grow sm:mt-auto md:mt-0 overflow-hidden">
      <!-- Render a single question page -->
      <template v-if="currentPage.type === 'single'">
        <Question :question="currentPage.questions[0]" v-model="responses[currentPage.questions[0].id]"
          class="mx-auto" />
      </template>

      <!-- Render a group page (list of questions, e.g. likert style) -->
      <template v-else-if="currentPage.type === 'group'">
        <div class="space-y-6">

          <div v-for="(question, index) in currentPage.questions" :key="question.id" ref="ratingRefs"
            :class="index === activeRatingIndex ? 'opacity-100' : 'opacity-50'">
            <Rating :question="question" v-model="responses[question.id]" @answered="handleAnswered(index)" />
          </div>
        </div>
      </template>
    </div>

    <!-- Navigation Buttons -->
    <div class="flex justify-between mt-6">
      <button @click="prevPage" :disabled="isFirstPage"
        class="px-4 py-3 rounded-lg bg-gray-700 hover:bg-gray-600 text-white disabled:opacity-50 disabled:cursor-not-allowed">
        이전
      </button>

      <!-- Next / Submit Button -->
      <button v-if="!isLastPage" @click="nextPage"
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
import Rating from "../components/ui/Rating.vue";

export default {
  name: "SurveyPage",
  components: { Question, Rating },
  data() {
    return {
      // questions fetched from API (unused in the final pages array)
      questions: [],
      // The user's answers keyed by question ID
      responses: {},
      // Navigation state (page index now instead of question index)
      currentPageIndex: 0,

      // Static selections
      surveyTypeId: 1,
      courseTypeId: 103,
      selectedPhase: "pre",

      // Will store grouped questions by category after fetching
      courseQuestions: {},
    };
  },
  computed: {
    activeRatingIndex() {
      if (this.currentPage.type !== 'group') return null;
      const idx = this.currentPage.questions.findIndex(q => !this.responses[q.id]);
      // If all questions have been answered, return the last question's index.
      return idx === -1 ? this.currentPage.questions.length - 1 : idx;
    },

    // Build pages where each page is either a "single" question page or a "group" of questions.
    pages() {
      // Start with the two static questions:
      const pages = [
        {
          type: "single",
          // We use a key like “surveyType” so that the v-model on Question will be responses["surveyType"]
          questions: [
            {
              id: "surveyType",
              text: "개인용 또는 기업용 설문을 선택하세요",
              question_type: "radio",
              options: [
                { id: 1, name: "개인용" },
                { id: 2, name: "기업용" },
              ],
            },
          ],
          // Optional title to show in the header
          pageTitle: "설문 유형 선택",
        },
        {
          type: "single",
          questions: [
            {
              id: "course",
              text: "참여하고 싶은 교육 과정을 선택하세요",
              question_type: "radio",
              options: this.getCourseOptions(),
            },
          ],
          pageTitle: "교육 과정 선택",
        },

      ];
      if (this.courseQuestions.demographic_personal) {
        this.courseQuestions.demographic_personal.forEach((question) => {
          pages.push({
            type: "single",
            questions: [question], // Single question per page
            pageTitle: "인구통계학",
          });
        });
      }

      // Now append pages for each category that was returned from the API.
      // (You can customise the order as needed.)
      for (const category in this.courseQuestions) {
        if (category !== "demographic_personal") {
          pages.push({
            type: "group",
            category, // the raw category key
            // Optionally, you could map the category key to a prettier title:
            categoryTitle: this.getCategoryTitle(category),
            questions: this.courseQuestions[category],
          });
        }
      }

      return pages;
    },
    currentPage() {
      return this.pages[this.currentPageIndex] || {};
    },
    progressWidth() {
      if (this.pages.length === 0) return 0;
      return ((this.currentPageIndex + 1) / this.pages.length) * 100;
    },
    isFirstPage() {
      return this.currentPageIndex === 0;
    },
    isLastPage() {
      return this.currentPageIndex === this.pages.length - 1;
    },
    // This can be used in the header – you might choose a title based on the page type.
    currentPageTitle() {
      if (this.currentPage.pageTitle) {
        return this.currentPage.pageTitle;
      } else if (this.currentPage.categoryTitle) {
        return this.currentPage.categoryTitle;
      }
      return "";
    },
  },
  watch: {
    // When surveyType or course selection changes, refetch the questions.
    "responses.surveyType"(newVal) {
      if (newVal) {
        this.surveyTypeId = parseInt(newVal);
        this.fetchQuestions();
      }
    },
    "responses.course"(newVal) {
      if (newVal) {
        this.courseTypeId = parseInt(newVal);
        this.fetchQuestions();
      }
    },
  },
  mounted() {
    this.fetchQuestions();
  },
  methods: {
    handleAnswered(index) {
      // Use $nextTick to wait for DOM updates
      this.$nextTick(() => {
        // Ensure we have an array of rating elements.
        const ratingElements = Array.isArray(this.$refs.ratingRefs)
          ? this.$refs.ratingRefs
          : [this.$refs.ratingRefs];

        // Loop from the next question to find the first unanswered question.
        for (let i = index + 1; i < this.currentPage.questions.length; i++) {
          const questionId = this.currentPage.questions[i].id;
          if (!this.responses[questionId]) {
            // Scroll the corresponding element into view
            const element = ratingElements[i];
            if (element) {
              element.scrollIntoView({ behavior: "smooth", block: "center" });
            }
            break;
          }
        }
      });
    },
    getCourseOptions() {
      if (this.responses.surveyType === 1) {
        // 개인용 (101, 103, 105)
        return [
          { id: 101, name: "비전하우스" },
          { id: 103, name: "자기 개발" },
          { id: 105, name: "커뮤니케이션" },
        ];
      } else if (this.responses.surveyType === 2) {
        // 기업용 (102, 104, 106)
        return [
          { id: 102, name: "경영 전략" },
          { id: 104, name: "리더십과 혁신" },
          { id: 106, name: "기업가정신과 혁신" },
        ];
      }
      return []; // Default if not selected
    },
    // Helper to map a raw category key to a display title
    getCategoryTitle(category) {
      // For example, you might have:
      const titles = {
        lifestyle: "라이프스타일",
        demographic_personal: "인구통계 (개인)",
        // Add more mappings as needed…
      };
      return titles[category] || category;
    },
    async fetchQuestions() {
      try {
        console.log("Fetching questions for:", this.surveyTypeId, this.courseTypeId);
        const url = `http://127.0.0.1:8000/api/survey/${this.surveyTypeId}/${this.courseTypeId}/`;
        const response = await fetch(url, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
        if (!response.ok) {
          console.error("Failed to fetch questions, status:", response.status);
          return;
        }
        const fetchedQuestions = await response.json();
        console.log("Fetched questions:", fetchedQuestions);

        // Group fetched questions by category.
        const grouped = {};
        fetchedQuestions.forEach((q) => {
          if (!grouped[q.category]) {
            grouped[q.category] = [];
          }
          grouped[q.category].push(q);
        });
        // Save to our reactive property.
        this.courseQuestions = grouped;

        // (Optional) Reset page index so the user isn’t thrown into a later page.
        // this.currentPageIndex = 0;
      } catch (err) {
        console.error("Error fetching questions:", err);
      }
    },
    nextPage() {
      if (!this.isLastPage) {
        this.currentPageIndex++;
      }
    },
    prevPage() {
      if (!this.isFirstPage) {
        this.currentPageIndex--;
      }
    },
    async submitSurvey() {
      try {
        // Convert the responses object into an array as expected by your backend.
        const answersArray = Object.entries(this.responses).map(([questionId, answerVal]) => {
          return {
            question_id: isNaN(questionId) ? questionId : parseInt(questionId),
            answer_text: typeof answerVal === "string" ? answerVal : null,
            answer_value: typeof answerVal === "number" ? answerVal : null,
          };
        });
        const bodyData = {
          phase: this.selectedPhase, // 'pre' or 'post'
          answers: answersArray,
        };
        const url = `/api/survey/${this.surveyTypeId}/${this.courseTypeId}/`;
        const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
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
.size-6 {
  width: 24px;
  height: 24px;
}
</style>