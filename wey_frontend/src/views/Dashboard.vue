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

      <!-- Dynamically Generated Demographic Charts -->
      <div v-for="category in demographicCategories" :key="category" class="mt-10">
        <h2 class="text-lg font-semibold text-gray-700">{{ category }} vs Survey Improvement</h2>
        <canvas :ref="(el) => setChartRef(el, category)"></canvas>
      </div>
    </main>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import { ref, reactive, onMounted, nextTick } from "vue";

Chart.register(...registerables);

export default {
  setup() {
    const leadershipChartInstance = ref(null);
    const demographicChartInstances = reactive({});
    const loading = ref(true);
    const errorMessage = ref("");
    const leadershipData = ref(null);
    const demographicData = reactive({});
    const demographicCategories = ["age", "salary", "education", "marital"];

    const fetchCompanyData = async () => {
      console.log("Fetching data for company ID:", window.location.pathname.split("/").pop());
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        console.error("❌ No authentication token found.");
        errorMessage.value = "Authentication token missing.";
        return;
      }

      try {
        // Fetch gender-leadership data
        const leadershipResponse = await fetch(
          `http://127.0.0.1:8000/api/companies/${window.location.pathname.split("/").pop()}/gender-leadership/`,
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );

        if (!leadershipResponse.ok) throw new Error(`API request failed.`);

        leadershipData.value = (await leadershipResponse.json()).data;

        // Fetch demographic data dynamically
        await fetchDemographicData(accessToken);

        nextTick(() => {
          renderLeadershipChart();
          renderDemographicCharts();
        });
      } catch (error) {
        console.error("❌ Failed to fetch company data:", error);
        errorMessage.value = "Failed to load company data.";
      } finally {
        loading.value = false;
      }
    };

    const fetchDemographicData = async (accessToken) => {
      try {
        const responses = await Promise.all(
          demographicCategories.map(async (category) => {
            const response = await fetch(
              `http://127.0.0.1:8000/api/dashboard/${window.location.pathname.split("/").pop()}/demographic-improvement/${category}/`,
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
        console.error("❌ Failed to fetch demographic data:", error);
      }
    };

    const renderLeadershipChart = () => {
      if (!leadershipData.value || leadershipData.value.length === 0) {
        console.warn("No data available for leadership chart.");
        return;
      }

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
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: "Average Rating" },
            },
          },
        },
      });
    };

    const renderDemographicCharts = () => {
      for (const category in demographicData) {
        const data = demographicData[category];

        if (!data || data.length === 0) {
          console.warn(`No data available for ${category} chart.`);
          continue;
        }

        const labels = data.map((entry) => entry[`${category}_group`]);
        const preData = data.map((entry) => entry.pre);
        const postData = data.map((entry) => entry.post);

        if (demographicChartInstances[category]) {
          demographicChartInstances[category].destroy();
        }

        const canvas = document.querySelector(`[ref="${category}Chart"]`);
        if (!canvas) {
          console.error(`❌ Missing ref for ${category}Chart`);
          continue;
        }

        const ctx = canvas.getContext("2d");
        demographicChartInstances[category] = new Chart(ctx, {
          type: "bar",
          data: {
            labels,
            datasets: [
              { label: "Pre Survey", data: preData, backgroundColor: "#FF5733" },
              { label: "Post Survey", data: postData, backgroundColor: "#33FF57" },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                title: { display: true, text: "Average Rating" },
              },
            },
          },
        });
      }
    };

    const setChartRef = (el, category) => {
      if (el) {
        demographicChartInstances[category] = el;
      }
    };

    onMounted(fetchCompanyData);

    return {
      leadershipChartInstance,
      demographicChartInstances,
      loading,
      errorMessage,
      leadershipData,
      demographicData,
      demographicCategories,
      setChartRef,
    };
  },
};
</script>
