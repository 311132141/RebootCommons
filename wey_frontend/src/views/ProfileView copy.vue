<template>
  <div class="container mx-auto px-8 py-6">
    <div class="bg-gray-900 text-white rounded-lg p-8 shadow-md flex items-center">
      <!-- Avatar -->
      <div class="w-32 h-32 bg-gray-700 rounded-lg flex items-center justify-center">
        <img v-if="user.avatar" :src="user.avatar" alt="User Avatar" class="w-full h-full object-cover rounded-lg" />
        <span v-else class="text-xl">No Avatar</span>
      </div>

      <!-- User Info -->
      <div class="ml-8">
        <h1 class="text-4xl font-bold text-gray-100">{{ user.name }}</h1>
        <ul class="mt-4 text-gray-300">
          <li><strong>Email:</strong> {{ user.email }}</li>
          <li><strong>성별:</strong> {{ user.demographics.gender }}</li>
          <li><strong>연령:</strong> {{ user.demographics.age }}</li>
          <li><strong>결혼 여부:</strong> {{ user.demographics.marital_status }}</li>
          <li><strong>학력:</strong> {{ user.demographics.education }}</li>
          <li><strong>소득 수준:</strong> {{ user.demographics.income }}</li>
        </ul>
        <!-- Selected Program -->
        <h2 class="text-xl font-semibold mt-6 text-gray-100">
          선택한 프로그램:
        </h2>
        <div>{{ user.demographics.selected_program }}</div>
      </div>
    </div>

    <!-- Pre/Post Growth Radar Chart -->
    <div class="mt-6">
      <h2 class="text-lg font-semibold text-gray-700">프로그램 참여 전후 비교</h2>
      <canvas ref="prePostRadarChart"></canvas>
    </div>

    <!-- User vs. All Growth Radar Chart -->
    <div class="mt-6">
      <h2 class="text-lg font-semibold text-gray-700">개인과 전체 평균 성장률 비교</h2>
      <canvas ref="userVsAllGrowthChart"></canvas>
    </div>

    <!-- Lifestyle vs Performance Heatmap -->
    <div class="mt-6">
      <h2 class="text-lg font-semibold text-gray-700">라이프스타일과 성장률의 상관관계</h2>
      <canvas ref="heatmapChart"></canvas>
    </div>

    <!-- Question Ratings Table -->
    <div class="mt-6">
      <h2 class="text-lg font-semibold text-gray-700">질문별 사용자 응답 비교</h2>
      <table class="table-auto w-full text-gray-700 border border-gray-300">
        <thead>
          <tr class="bg-gray-200">
            <th class="px-4 py-2">카테고리</th>
            <th class="px-4 py-2">질문</th>
            <th class="px-4 py-2">사전 응답</th>
            <th class="px-4 py-2">사후 응답</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(question, index) in questionRatings" :key="index" class="border-b">
            <td class="px-4 py-2">{{ question.category }}</td>
            <td class="px-4 py-2">{{ question.question }}</td>
            <td class="px-4 py-2">{{ question.pre_score }}</td>
            <td class="px-4 py-2">{{ question.post_score }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Question-Level Radar Charts -->
    <div class="mt-6">
      <h2 class="text-lg font-semibold text-gray-700">카테고리별 질문 비교</h2>
      <div v-for="(category, index) in questionGrowthData.categories" :key="index" class="mb-6">
        <h3 class="text-md font-semibold text-gray-600">{{ category.name }}</h3>
        <canvas :ref="el => questionRadarCharts[index] = el"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { Chart, registerables } from "chart.js";
import "chartjs-chart-matrix";

Chart.register(...registerables);

export default {
  setup() {
    const route = useRoute();
    const user = ref({
      name: "",
      email: "",
      avatar: null,
      demographics: {}
    });

    // Canvas refs for charts
    const prePostRadarChart = ref(null);
    const userVsAllGrowthChart = ref(null);
    const heatmapChart = ref(null);
    const questionRadarCharts = ref([]);

    // Reactive properties for question-level data
    const questionRatings = ref([]);
    const questionGrowthData = ref({ categories: [] });

    // Fetch user profile
    const fetchUserProfile = async () => {
      const userId = route.params.id;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/profile/`);
        user.value = response.data;
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    };

    // Fetch pre/post growth data (for radar chart)
    const fetchPrePostData = async () => {
      const userId = route.params.id;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/pre-post-comparison/`);
        if (!response.data.categories || response.data.categories.length === 0) {
          console.warn("No pre/post data returned");
          return;
        }
        renderRadarChart(prePostRadarChart.value, response.data, "Pre-Lecture", "Post-Lecture");
      } catch (error) {
        console.error("Error fetching pre/post data:", error);
      }
    };

    // Fetch user vs all growth data (for radar chart)
    const fetchUserVsAllGrowth = async () => {
      const userId = route.params.id;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/user-growth-comparison/`);
        if (!response.data.categories || response.data.categories.length === 0) {
          console.warn("No user vs all growth data returned");
          return;
        }
        renderRadarChart(userVsAllGrowthChart.value, response.data, "User Growth", "All Users Growth");
      } catch (error) {
        console.error("Error fetching user vs all growth data:", error);
      }
    };

    // Fetch heatmap data
    const fetchHeatmapData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/dashboard/lifestyle-performance-growth/all/`);
        if (!response.data || !response.data.data || response.data.data.length === 0) {
          console.warn("No heatmap data returned");
          return;
        }
        renderHeatmap(heatmapChart.value, response.data);
      } catch (error) {
        console.error("Error fetching heatmap data:", error);
      }
    };

    // Fetch question ratings and question-level data
    const fetchQuestionRatings = async () => {
      const userId = route.params.id;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/question-pre-post-comparison/`);
        // Expected format: { categories: [ { name, questions: [ { question, pre_score, post_score } ] } ] }
        questionGrowthData.value = response.data;
        // Flatten the data for table display:
        questionRatings.value = response.data.categories.flatMap(cat =>
          cat.questions.map(q => ({
            category: cat.name,
            question: q.question,
            pre_score: q.pre_score,
            post_score: q.post_score
          }))
        );
        renderQuestionRadarCharts(response.data.categories);
      } catch (error) {
        console.error("Error fetching question ratings data:", error);
      }
    };

    // Generic function to render a radar chart on a given canvas
    const renderRadarChart = (canvas, data, label1, label2) => {
      if (!canvas || !data || !data.categories) {
        console.warn("No data for radar chart");
        return;
      }
      const ctx = canvas.getContext("2d");
      new Chart(ctx, {
        type: "radar",
        data: {
          labels: data.categories,
          datasets: [
            {
              label: label1,
              data: data.pre_scores || data.user_scores,
              borderColor: "#FF0000",
              backgroundColor: "rgba(255, 0, 0, 0.2)",
              fill: true,
            },
            {
              label: label2,
              data: data.post_scores || data.all_users_scores,
              borderColor: "#FFFF00",
              backgroundColor: "rgba(255, 255, 0, 0.2)",
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            r: {
              beginAtZero: true,
              suggestedMax: 100,
            },
          },
        },
      });
    };

    // Function to render a heatmap
    const renderHeatmap = (canvas, data) => {
      if (!canvas || !data || !data.data || data.data.length === 0) {
        console.warn("No data for heatmap");
        return;
      }
      const ctx = canvas.getContext("2d");
      new Chart(ctx, {
        type: "matrix",
        data: {
          datasets: [
            {
              label: "Lifestyle vs Performance Growth",
              data: data.data.map(item => ({
                x: item.question,
                y: item.rating,
                v: item.growth,
              })),
              backgroundColor: (ctx) => {
                const value = ctx.raw.v;
                return value > 20
                  ? "red"
                  : value > 10
                    ? "orange"
                    : value > 5
                      ? "yellow"
                      : value > 0
                        ? "green"
                        : "blue";
              },
            },
          ],
        },
        options: {
          scales: {
            x: { type: "category" },
            y: { type: "linear", min: 1, max: 5 },
          },
        },
      });
    };

    // Render question-level radar charts for each category
    const renderQuestionRadarCharts = (categories) => {
      categories.forEach((cat, index) => {
        const canvas = questionRadarCharts.value[index];
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        new Chart(ctx, {
          type: "radar",
          data: {
            labels: cat.questions.map((q) => q.question),
            datasets: [
              {
                label: "Pre-Lecture",
                data: cat.questions.map((q) => q.pre_score),
                borderColor: "#FF0000",
                backgroundColor: "rgba(255, 0, 0, 0.2)",
                fill: true,
              },
              {
                label: "Post-Lecture",
                data: cat.questions.map((q) => q.post_score),
                borderColor: "#FFFF00",
                backgroundColor: "rgba(255, 255, 0, 0.2)",
                fill: true,
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              r: {
                beginAtZero: true,
                suggestedMax: 100,
              },
            },
          },
        });
      });
    };

    onMounted(async () => {
      await fetchUserProfile();
      await fetchPrePostData();
      await fetchUserVsAllGrowth();
      await fetchHeatmapData();
      await fetchQuestionRatings();
    });

    return {
      user,
      prePostRadarChart,
      userVsAllGrowthChart,
      heatmapChart,
      questionRadarCharts,
      questionRatings,
      questionGrowthData,
    };
  },
};
</script>