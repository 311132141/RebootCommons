<template>
  <div class="sm:ml-64 min-h-screen bg-gray-50">
    <main class="p-6">
      <!-- Page Header -->
      <div class="text-3xl font-bold text-gray-800 mb-4">Company Dashboard</div>

      <!-- Loading / Error Messages -->
      <p v-if="loading" class="text-gray-500">Loading data...</p>
      <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

      <!-- Dash Cards -->
      <div class="grid grid-cols-12 gap-5 pb-5" v-if="!loading">
        <div class="col-span-4 p-4 bg-white rounded shadow text-center">
          <h2 class="text-xl font-semibold">참가자 수</h2>
          <p class="text-2xl">{{ dashCardData.participants }}</p>
        </div>
        <div class="col-span-4 p-4 bg-white rounded shadow text-center">
          <h2 class="text-xl font-semibold">평균 성장률</h2>
          <p class="text-2xl">{{ dashCardData.improvementPercentage }}%</p>
        </div>
        <div class="col-span-4 p-4 bg-white rounded shadow text-center">
          <h2 class="text-xl font-semibold">선택 교육 과정</h2>
          <p class="text-2xl">{{ dashCardData.selectedCourse }}</p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="space-y-10">
        <!-- Row 1: Gender Distribution and Leadership Comparison -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12 md:col-span-12 lg:col-span-5">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">성별 분포</h2>
              <!-- Plain canvas element for gender distribution chart -->
              <canvas id="genderDistributionChart"></canvas>
            </div>
          </div>
          <div class="col-span-12 md:col-span-12 lg:col-span-7">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">남성, 여성 리더십 비교</h2>
              <ChartCard_pie title="성별 분포" description="각 프로그램에 등록한 총 참가자 수와 평균 성장률을 시각화합니다."
                :chartData="genderDistributionData" :chartOptions="genderDistributionOptions"
                :labels="genderDistributionData.labels" :data="genderDistributionData.datasets[0].data"
                label_name="참가자 수" />
            </div>
          </div>
        </div>

        <!-- Row 2: Age Distribution and Age Improvement Comparison -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12 md:col-span-12 lg:col-span-5">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">연령대 분포</h2>
              <canvas id="ageDistributionChart"></canvas>
            </div>
          </div>
          <div class="col-span-12 md:col-span-12 lg:col-span-7">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">연령대별 성장률 비교</h2>
              <canvas id="ageImprovementChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Row 3: Job Distribution and Job Salary Comparison -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12 md:col-span-12 lg:col-span-5">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">직무 및 직책 분포</h2>
              <canvas id="jobDistributionChart"></canvas>
            </div>
          </div>
          <div class="col-span-12 md:col-span-12 lg:col-span-7">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">직무 직책과 연봉 비교</h2>
              <canvas id="jobSalaryChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Row 4: Department Growth Comparison -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">직군, 직급, 근속 기간으로 성장률 비교</h2>
              <canvas id="departmentGrowthChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Row 5: Company vs Overall Comparison -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">회사와 전체 평균 비교</h2>
              <canvas id="companyComparisonChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Row 6: Program Comparison -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">프로그램별 참가자수와 성장률 비교</h2>
              <p class="text-sm text-gray-600 mt-1">
                예를 들어, 리더십과 혁신 프로그램은 참가자 40%가 등록했으며, 평균 성장률은 +10.5%로 가장 높은 효과를 보였습니다.
              </p>
              <canvas id="programComparisonChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Row 7: Before/After Comparison and Lifestyle vs Growth -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12 md:col-span-12 lg:col-span-6">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">주요 성장 지표의 사전/사후 비교</h2>
              <canvas id="beforeAfterChart"></canvas>
            </div>
          </div>
          <div class="col-span-12 md:col-span-12 lg:col-span-6">
            <div class="bg-white p-4 rounded shadow">
              <h2 class="text-lg font-semibold text-gray-700 mb-2">라이프스타일 지표와 성과 성장 간 관계</h2>
              <canvas id="lifestyleVsGrowthChart"></canvas>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

// -------------------------------
// Reactive States & Chart Options
// -------------------------------
const dashCardData = ref({
  participants: 0,
  improvementPercentage: 0,
  selectedCourse: ""
});
const loading = ref(true);
const errorMessage = ref("");

const leadershipData = ref(null);
const leadershipChartInstance = ref(null);

const demographicData = reactive({});
const demographicChartInstances = reactive({});
const demographicCategories = ['age', 'salary', 'education', 'marital'];

const genderDistributionData = ref(null);
const genderDistributionOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const leadershipComparisonData = ref(null);
const leadershipComparisonOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const ageDistributionData = ref(null);
const ageDistributionOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const ageImprovementData = ref(null);
const ageImprovementOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const jobDistributionData = ref(null);
const jobDistributionOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const jobSalaryData = ref(null);
const jobSalaryOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const departmentGrowthData = ref(null);
const departmentGrowthOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const companyComparisonData = ref(null);
const companyComparisonOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const programComparisonData = ref(null);
const programComparisonOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const beforeAfterChartData = ref(null);
const beforeAfterChartOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

const lifestyleVsGrowthData = ref(null);
const lifestyleVsGrowthOptions = { responsive: true, plugins: { legend: { display: true, position: 'top' } } };

// -------------------------------
// Helper: Map demographic keys to display names
// -------------------------------
const getDisplayCategory = (cat) => {
  const mapping = {
    age: "Age Distribution",
    salary: "Salary Distribution",
    education: "Education Level",
    marital: "Marital Status"
  };
  return mapping[cat] || cat;
};

// -------------------------------
// Data Fetching Functions (individual try/catch blocks)
// -------------------------------

const fetchDashCardData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/dashboard/dashcard", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch dash card data.");
    dashCardData.value = await response.json();
  } catch (error) {
    console.error("Error fetching dash card data:", error);
  }
};

const fetchGenderDistributionData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/gender-distribution/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch gender distribution data.");
    genderDistributionData.value = await response.json();
  } catch (error) {
    console.error("Error fetching gender distribution data:", error);
  }
};

const fetchLeadershipComparisonData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/male-female-leadership/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch leadership comparison data.");
    leadershipComparisonData.value = await response.json();
  } catch (error) {
    console.error("Error fetching leadership comparison data:", error);
  }
};

const fetchAgeDistributionData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/age-distribution/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch age distribution data.");
    ageDistributionData.value = await response.json();
  } catch (error) {
    console.error("Error fetching age distribution data:", error);
  }
};

const fetchAgeImprovementData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    // If you have a dedicated age improvement endpoint, ensure it exists.
    const response = await fetch("http://127.0.0.1:8000/api/graphs/age-improvement/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch age improvement data.");
    ageImprovementData.value = await response.json();
  } catch (error) {
    console.error("Error fetching age improvement data:", error);
  }
};

const fetchJobDistributionData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/job-distribution/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch job distribution data.");
    jobDistributionData.value = await response.json();
  } catch (error) {
    console.error("Error fetching job distribution data:", error);
  }
};

const fetchJobSalaryData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/job-salary/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch job salary data.");
    jobSalaryData.value = await response.json();
  } catch (error) {
    console.error("Error fetching job salary data:", error);
  }
};

const fetchDepartmentGrowthData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/department-growth/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch department growth data.");
    departmentGrowthData.value = await response.json();
  } catch (error) {
    console.error("Error fetching department growth data:", error);
  }
};

const fetchCompanyComparisonData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/company-comparison/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch company comparison data.");
    companyComparisonData.value = await response.json();
  } catch (error) {
    console.error("Error fetching company comparison data:", error);
  }
};

const fetchProgramComparisonData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/program-comparison/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch program comparison data.");
    programComparisonData.value = await response.json();
  } catch (error) {
    console.error("Error fetching program comparison data:", error);
  }
};

const fetchBeforeAfterChartData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/pre-post-comparison/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch before-after chart data.");
    beforeAfterChartData.value = await response.json();
  } catch (error) {
    console.error("Error fetching before-after chart data:", error);
  }
};

const fetchLifestyleVsGrowthData = async () => {
  try {
    const accessToken = localStorage.getItem("access_token");
    const response = await fetch("http://127.0.0.1:8000/api/graphs/lifestyle-vs-growth/", {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!response.ok) throw new Error("Failed to fetch lifestyle vs growth data.");
    lifestyleVsGrowthData.value = await response.json();
  } catch (error) {
    console.error("Error fetching lifestyle vs growth data:", error);
  }
};

const fetchLeadershipData = async () => {
  try {
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
    // Assumes the API returns an object with a "data" property.
    leadershipData.value = (await response.json()).data;
  } catch (error) {
    console.error(error);
    errorMessage.value = "Error fetching leadership data.";
  }
};

// -------------------------------
// Chart Rendering Functions (using Chart.js)
// -------------------------------
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
      scales: { y: { beginAtZero: true, title: { display: true, text: 'Average Rating' } } }
    }
  });
};

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
        scales: { y: { beginAtZero: true, title: { display: true, text: 'Average Rating' } } }
      }
    });
  });
};

// -------------------------------
// onMounted: Fetch Data and Render Charts
// -------------------------------
onMounted(async () => {
  await Promise.all([
    fetchDashCardData(),
    fetchGenderDistributionData(),
    fetchLeadershipComparisonData(),
    fetchAgeDistributionData(),
    fetchAgeImprovementData(),
    fetchJobDistributionData(),
    fetchJobSalaryData(),
    fetchDepartmentGrowthData(),
    fetchCompanyComparisonData(),
    fetchProgramComparisonData(),
    fetchBeforeAfterChartData(),
    fetchLifestyleVsGrowthData(),
    fetchLeadershipData()
  ]);
  nextTick(() => {
    renderLeadershipChart();
    renderDemographicCharts();
    loading.value = false;
  });
});
</script>

<style scoped>
body {
  font-family: "Inter", sans-serif;
}

canvas {
  max-width: 100%;
  height: auto;
}
</style>