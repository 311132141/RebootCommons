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
          <div class="text-xl font-bold mb-4">{{ currentPage.categoryTitle }}</div>
          <div v-for="question in currentPage.questions" :key="question.id">
            <Rating :question="question" v-model="responses[question.id]" />
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
import { useUserStore } from "@/stores/user";

export default {
  name: "SurveyPage",
  components: { Question, Rating },
  setup() {
    const userStore = useUserStore();
    console.log("🟢 User Store Initialized:", userStore); // ✅ Debugging output

    return { userStore };
  },
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
      console.log("📢 SurveyType changed:", newVal); // Debugging
      if (newVal) {
        this.surveyTypeId = parseInt(newVal);
        // console.log("📢 Fetching questions for SurveyType ID:", this.surveyTypeId);
        // this.fetchQuestions();
        this.courseTypeId = null; // Reset course selection
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
    getCourseOptions() {
      console.log("📢 SurveyType ID when getting courses:", this.responses.surveyType);
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

        // 🔹 Get token from Local Storage (if Pinia store is empty)
        let accessToken = this.userStore?.user?.access || localStorage.getItem("access_token");

        if (!accessToken) {
          console.error("❌ No authentication token found.");
          alert("User is not authenticated. Please log in again.");
          return;
        }

        const url = `http://127.0.0.1:8000/api/survey/${this.surveyTypeId}/${this.courseTypeId}/`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken}`, // ✅ Ensure token is included
          },
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
      // First, try getting user info from userStore
      let userInfo = this.userStore?.userInfo;

      // If userStore is empty (e.g., after refresh), load from localStorage
      if (!userInfo) {
        console.log("⚠️ User info not found in userStore, checking Local Storage...");
        const storedUser = localStorage.getItem("user_info");
        if (storedUser) {
          userInfo = JSON.parse(storedUser); // ✅ Convert JSON string back to an object
        }
      }
      if (!userInfo || !userInfo.id) {
        console.error("❌ No User Info found! Please log in again.");
        alert("User info is missing. Please log in again.");
        return;
      }

      console.log("🟢 Using stored user info:", userInfo);
      try {
        // Convert the responses object into an array
        const answersArray = Object.entries(this.responses)
          .filter(([questionId]) => !isNaN(questionId))  // 🚀 Remove "surveyType" and "course"
          .map(([questionId, answerVal]) => {

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

        console.log("🟢 Submitting survey with data:", bodyData);

        const url = `http://127.0.0.1:8000/api/survey/${this.surveyTypeId}/${this.courseTypeId}/`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + this.userStore?.user?.access, // Ensure token is sent
          },
          body: JSON.stringify(bodyData),
        });

        console.log("🟡 Response received:", response);

        const result = await response.json();
        console.log("🟢 Survey submission response:", result);

        if (response.ok) {
          alert("설문이 제출되었습니다. 감사합니다!");
        } else {
          alert("설문 제출에 실패했습니다.");
        }
      } catch (err) {
        console.error("Error submitting survey:", err);
      }
    }

  },
};
</script>

<style scoped>
.size-6 {
  width: 24px;
  height: 24px;
}
</style>