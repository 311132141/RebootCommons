<template>
  <div class="sm:ml-64">
    <main>
      <h1 class="text-2xl font-bold text-gray-800">Company Dashboard</h1>
      <p v-if="loading" class="text-gray-500">Loading data...</p>
      <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

      <!-- Gender vs Leadership Chart -->
      <div class="mt-6">
        <h2 class="text-lg font-semibold text-gray-700">Gender vs Leadership</h2>
        <canvas ref="leadershipChart"></canvas>
      </div>

      <!-- Company vs Industry Growth Comparison -->
      <div class="mt-10">
        <h2 class="text-lg font-semibold text-gray-700">회사 vs. 업계 비교</h2>
        <canvas ref="growthChart"></canvas>
      </div>

      <!-- Dynamically Generated Demographic Charts -->
      <div v-for="category in demographicCategories" :key="category" class="mt-10">
        <h2 class="text-lg font-semibold text-gray-700">{{ category }} vs Survey Improvement</h2>
        <canvas :ref="(el) => setChartRef(el, category)"></canvas>
      </div>

      <!-- Lifestyle vs Performance Growth Heatmap -->
      <div class="mt-10">
        <h2 class="text-lg font-semibold text-gray-700">Lifestyle vs Performance Growth</h2>
        <canvas ref="heatmapChart"></canvas>
      </div>
    </main>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import "chartjs-chart-matrix";
import { ref, reactive, onMounted, nextTick } from "vue";

Chart.register(...registerables);

export default {
  setup() {
    const leadershipChartInstance = ref(null);
    const growthChartInstance = ref(null);
    const demographicChartInstances = reactive({});
    const loading = ref(true);
    const errorMessage = ref("");
    const leadershipData = ref(null);
    const growthData = ref(null);
    const demographicData = reactive({});
    const demographicCategories = ["age", "salary", "education", "marital"];

    const fetchCompanyData = async () => {
      const companyId = window.location.pathname.split("/").pop();
      console.log("Fetching data for company ID:", companyId);
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        console.error("No authentication token found.");
        errorMessage.value = "Authentication token missing.";
        return;
      }

      try {
        // Fetch gender-leadership data
        console.log("Fetching gender vs leadership data...");
        const leadershipResponse = await fetch(
          `http://127.0.0.1:8000/api/companies/${companyId}/gender-leadership/`,
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );
        if (!leadershipResponse.ok) throw new Error("API request failed.");
        leadershipData.value = (await leadershipResponse.json()).data;
        console.log("✅ Gender vs Leadership Data:", leadershipData.value);

        // Fetch company vs industry growth data
        console.log("Fetching company vs industry growth data...");
        const growthResponse = await fetch(
          `http://127.0.0.1:8000/api/dashboard/${companyId}/growth-comparison/`,
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );
        if (!growthResponse.ok) throw new Error("Failed to fetch growth data.");
        growthData.value = await growthResponse.json();
        console.log("✅ Company vs Industry Growth Data:", growthData.value);

        // Fetch demographic data dynamically
        await fetchDemographicData(accessToken);

        nextTick(() => {
          renderLeadershipChart();
          renderGrowthChart();
          renderDemographicCharts();
        });
      } catch (error) {
        console.error("Failed to fetch company data:", error);
        errorMessage.value = "Failed to load company data.";
      } finally {
        loading.value = false;
      }

      // Fetch lifestyle vs performance heatmap data
      
    };

    const fetchDemographicData = async (accessToken) => {
      try {
        const companyId = window.location.pathname.split("/").pop();
        console.log("Fetching demographic data...");
        const responses = await Promise.all(
          demographicCategories.map(async (category) => {
            const response = await fetch(
              `http://127.0.0.1:8000/api/dashboard/${companyId}/demographic-improvement/${category}/`,
              { headers: { Authorization: `Bearer ${accessToken}` } }
            );
            if (!response.ok) throw new Error(`Failed to fetch ${category} data.`);
            return { category, data: await response.json() };
          })
        );

        // Populate demographicData
        responses.forEach(({ category, data }) => {
          demographicData[category] = data.data;
        });

        console.log("✅ Demographic API Responses:", demographicData);
      } catch (error) {
        console.error("Failed to fetch demographic data:", error);
      }
    };

    const renderLeadershipChart = () => {
      if (!leadershipData.value || leadershipData.value.length === 0) {
        console.warn("No data available for leadership chart.");
        return;
      }

      console.log("Rendering Leadership Chart...");
      const labels = leadershipData.value.map((entry) => entry.category);
      const maleData = leadershipData.value.map((entry) => entry["남성"]);
      const femaleData = leadershipData.value.map((entry) => entry["여성"]);

      if (leadershipChartInstance.value) {
        leadershipChartInstance.value.destroy();
      }

      const ctx = document.querySelector("[ref='leadershipChart']").getContext("2d");
      leadershipChartInstance.value = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            { label: "남성 (Male)", data: maleData, backgroundColor: "#4F46E5" },
            { label: "여성 (Female)", data: femaleData, backgroundColor: "#A78BFA" },
          ],
        },
        options: { responsive: true },
      });
    };

    const renderGrowthChart = () => {
      if (!growthData.value || !growthData.value.categories) {
        console.warn("No data available for growth chart.");
        return;
      }

      console.log("Rendering Growth Chart...");
      console.log("Growth Chart Data:", growthData.value);

      // Extract raw data from Vue Proxy
      const categories = [...growthData.value.categories];
      const companyScores = [...growthData.value.company_scores];
      const industryScores = [...growthData.value.industry_scores];

      if (growthChartInstance.value) {
        growthChartInstance.value.destroy();
      }

      const canvas = document.querySelector("[ref='growthChart']");
      if (!canvas) {
        console.error("❌ Growth chart canvas not found.");
        return;
      }

      const ctx = canvas.getContext("2d");
      growthChartInstance.value = new Chart(ctx, {
        type: "radar",
        data: {
          labels: categories,  // Ensure extracted raw data
          datasets: [
            { label: "Company Growth", data: companyScores, borderColor: "yellow", fill: false },
            { label: "Industry Growth", data: industryScores, borderColor: "red", fill: false },
          ],
        },
        options: { responsive: true, scales: { r: { beginAtZero: true, max: 100 } } },
      });
    };


    const setChartRef = (el, category) => {
      if (el) {
        demographicChartInstances[category] = el;
      }
    };

    onMounted(fetchCompanyData);

    return {
      leadershipChartInstance,
      growthChartInstance,
      demographicChartInstances,
      loading,
      errorMessage,
      leadershipData,
      growthData,
      demographicData,
      demographicCategories,
      setChartRef,
    };
  
  
  },
  setup() {
    const heatmapChart = ref(null);
    const heatmapData = ref([]);
    const loading = ref(true);
    const errorMessage = ref("");

    const fetchHeatmapData = async () => {
      console.log("Fetching lifestyle vs performance growth data...");
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        console.error("❌ No authentication token found.");
        errorMessage.value = "Authentication token missing.";
        return;
      }

      try {
        const companyId = window.location.pathname.split("/").pop();
        const response = await fetch(
          `http://127.0.0.1:8000/api/dashboard/${companyId}/lifestyle-performance-growth/`,
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );

        if (!response.ok) throw new Error("API request failed.");

        const result = await response.json();
        heatmapData.value = result.data;

        console.log("✅ Heatmap API Response:", heatmapData.value);

        nextTick(() => {
          renderHeatmap();
        });
      } catch (error) {
        console.error("❌ Failed to fetch heatmap data:", error);
        errorMessage.value = "Failed to load heatmap data.";
      } finally {
        loading.value = false;
      }
    };

    const renderHeatmap = () => {
      if (!heatmapData.value.length) {
        console.warn("⚠️ No heatmap data available.");
        return;
      }

      const questions = [...new Set(heatmapData.value.map((d) => d.question))];
      const ratings = [1, 2, 3, 4, 5];

      // Transform data into matrix format
      const matrixData = heatmapData.value.map((d) => ({
        x: questions.indexOf(d.question),
        y: ratings.indexOf(d.rating) + 1,
        v: d.growth,
      }));

      if (heatmapChart.value) {
        heatmapChart.value.destroy();
      }

      const ctx = document.querySelector("[ref='heatmapChart']").getContext("2d");
      heatmapChart.value = new Chart(ctx, {
        type: "matrix",
        data: {
          datasets: [
            {
              label: "Growth %",
              data: matrixData,
              backgroundColor: (ctx) => {
                const value = ctx.raw.v;
                if (value > 15) return "red";
                if (value > 10) return "orange";
                if (value > 5) return "yellow";
                return "green";
              },
              width: ({ chart }) => (chart.chartArea || {}).width / questions.length - 2,
              height: ({ chart }) => (chart.chartArea || {}).height / ratings.length - 2,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              type: "category",
              labels: questions,
              title: { display: true, text: "Lifestyle Questions" },
            },
            y: {
              type: "linear",
              min: 1,
              max: 5,
              title: { display: true, text: "Ratings" },
            },
          },
          plugins: {
            tooltip: {
              callbacks: {
                title: (ctx) => `Rating: ${ctx[0].raw.y}`,
                label: (ctx) => `Growth: ${ctx.raw.v.toFixed(2)}%`,
              },
            },
          },
        },
      });
    };

    onMounted(fetchHeatmapData);

    return {
      heatmapChart,
      heatmapData,
      loading,
      errorMessage,
    };
  },
};
</script>
