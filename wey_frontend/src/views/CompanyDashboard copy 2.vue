<template>
  <div class="sm:ml-64 min-h-screen bg-gray-50">
    <main class="p-6">
      <h1 class="text-3xl font-bold text-gray-800 mb-4">Company Dashboard</h1>

      <!-- Loading / Error Messages -->
      <p v-if="loading" class="text-gray-500">Loading data...</p>
      <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

      <!-- Overview Cards (Example DashCards) -->
      <div class="grid grid-cols-12 gap-5 pb-5" v-if="!loading">
        <!-- Replace these with your own DashCard components if needed -->
        <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 1</div>
        <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 2</div>
        <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 3</div>
        <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 4</div>
      </div>

      <!-- Charts Section -->
      <div class="space-y-10">
        <!-- 1. Gender vs Leadership Chart -->
        <section class="mt-6">
          <h2 class="text-xl font-semibold text-gray-700 mb-2">Gender vs Leadership</h2>
          <div class="bg-white p-4 rounded shadow">
            <canvas id="leadershipChart"></canvas>
          </div>
        </section>

        <!-- 2. Dynamically Generated Demographic Charts -->
        <section class="mt-10" v-for="category in demographicCategories" :key="category">
          <h2 class="text-xl font-semibold text-gray-700 mb-2">
            {{ getDisplayCategory(category) }} vs Survey Improvement
          </h2>
          <div class="bg-white p-4 rounded shadow">
            <canvas :id="`${category}Chart`"></canvas>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

// Reactive states
const loading = ref(true);
const errorMessage = ref('');
const leadershipData = ref(null);
const leadershipChartInstance = ref(null);
const demographicData = reactive({});
const demographicChartInstances = reactive({});
// Adjust these categories as needed (they should match your backend endpoint names)
const demographicCategories = ['age', 'salary', 'education', 'marital'];

// Helper to map raw category keys to display names
const getDisplayCategory = (cat) => {
  const mapping = {
    age: "Age Distribution",
    salary: "Salary Distribution",
    education: "Education Level",
    marital: "Marital Status",
  };
  return mapping[cat] || cat;
};

// Fetch leadership data from the backend
const fetchLeadershipData = async () => {
  try {
    // Assumes the company ID is the last segment of the URL
    const companyId = window.location.pathname.split("/").pop();
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      errorMessage.value = "Authentication token missing.";
      return;
    }
    const response = await fetch(`http://127.0.0.1:8000/api/companies/${companyId}/gender-leadership/`, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error('Failed to fetch leadership data.');
    // Assuming the API returns an object with a "data" property
    leadershipData.value = (await response.json()).data;
  } catch (error) {
    console.error(error);
    errorMessage.value = "Error fetching leadership data.";
  }
};

// Fetch demographic data for each category from the backend
const fetchDemographicData = async () => {
  try {
    const companyId = window.location.pathname.split("/").pop();
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      errorMessage.value = "Authentication token missing.";
      return;
    }
    await Promise.all(
      demographicCategories.map(async (category) => {
        const response = await fetch(
          `http://127.0.0.1:8000/api/dashboard/${companyId}/demographic-improvement/${category}/`,
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );
        if (!response.ok) throw new Error(`Failed to fetch ${category} data.`);
        const json = await response.json();
        // Assumes the API returns an object with a "data" property
        demographicData[category] = json.data;
      })
    );
  } catch (error) {
    console.error(error);
    errorMessage.value = "Error fetching demographic data.";
  }
};

// Render the leadership chart using Chart.js
const renderLeadershipChart = () => {
  if (!leadershipData.value || leadershipData.value.length === 0) {
    console.warn("No leadership data available.");
    return;
  }
  const labels = leadershipData.value.map(entry => entry.category);
  const maleData = leadershipData.value.map(entry => entry['남성']);
  const femaleData = leadershipData.value.map(entry => entry['여성']);

  const ctx = document.getElementById('leadershipChart').getContext('2d');
  if (leadershipChartInstance.value) {
    leadershipChartInstance.value.destroy();
  }
  leadershipChartInstance.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: '남성 (Male)', data: maleData, backgroundColor: '#4F46E5' },
        { label: '여성 (Female)', data: femaleData, backgroundColor: '#A78BFA' }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Average Rating' } }
      }
    }
  });
};

// Render each demographic chart using Chart.js
const renderDemographicCharts = () => {
  Object.keys(demographicData).forEach(category => {
    const data = demographicData[category];
    if (!data || data.length === 0) {
      console.warn(`No data available for ${category} chart.`);
      return;
    }
    const labels = data.map(entry => entry[`${category}_group`]);
    const preData = data.map(entry => entry.pre);
    const postData = data.map(entry => entry.post);
    const canvas = document.getElementById(`${category}Chart`);
    if (!canvas) {
      console.error(`Missing canvas element for ${category}Chart`);
      return;
    }
    const ctx = canvas.getContext('2d');
    // If a previous instance exists, destroy it before creating a new one.
    if (demographicChartInstances[category]) {
      demographicChartInstances[category].destroy();
    }
    demographicChartInstances[category] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          { label: 'Pre Survey', data: preData, backgroundColor: '#FF5733' },
          { label: 'Post Survey', data: postData, backgroundColor: '#33FF57' }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true, title: { display: true, text: 'Average Rating' } }
        }
      }
    });
  });
};

// On component mount, fetch backend data and render charts
onMounted(async () => {
  await fetchLeadershipData();
  await fetchDemographicData();
  // Wait for the DOM to update before rendering charts
  nextTick(() => {
    renderLeadershipChart();
    renderDemographicCharts();
    loading.value = false;
  });
});
</script>

<style scoped>
/* Optional styling adjustments */
body {
  font-family: "Inter", sans-serif;
}

canvas {
  /* Ensure the charts are responsive */
  max-width: 100%;
  height: auto;
}
</style>