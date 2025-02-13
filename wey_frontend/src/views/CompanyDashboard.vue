<template>

  <div class="flex h-screen" v-if="!loading">


    <!-- Main Content -->

    <!-- Navbar -->
    <main class="flex-1 p-6 ">
      <div class="flex items-center justify-between mb-6 print:hidden">
        <div class="flex items-center space-x-2 text-gray-400 ">
          <span>Dashboard</span>
          <span>></span>
          <span>Companies</span>
        </div>
        <div class="flex items-center space-x-4 ">
          <button @click="printDashboard"
            class=" bg-gray-800 p-2 rounded-md text-white px-4 py-2 rounded hover:bg-blue-600 print:hidden">
            리포트 작성하기
          </button>
          <!-- <div class="relative">
              <input type="text" placeholder="Search"
                class="bg-[#25262b] rounded-md px-4 py-2 pl-10 text-sm w-64 focus:outline-none" />
              <svg class="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none"
                stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div> -->
          <!-- <button class="bg-gray-800 p-2 rounded-md">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
            </button> -->
        </div>
      </div>
      <h1 class="text-2xl text-bold pb-3 print:text-black mb-6 print:mb-6">Overview</h1>

      <!-- <router-view /> -->
      <div class="grid grid-cols-12 gap-5 pb-5 print:hidden">
        <DashCard />
        <DashCard />
        <DashCard />
        <DashCard />
      </div>
      <!-- Loading / Error Messages -->
      <p v-if="loading" class="text-gray-500">Loading data...</p>
      <p v-if="errorMessage" class="text-red-500 print:hidden">{{ errorMessage }}</p>

      <!-- Overview Cards (Example DashCards) -->
      <!-- <div class="grid grid-cols-12 gap-5 pb-5" v-if="!loading">
   
          <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 1</div>
          <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 2</div>
          <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 3</div>
          <div class="col-span-3 p-4 bg-white rounded shadow">DashCard 4</div>
        </div> -->

      <!-- Charts Section -->
      <div class="space-y-6">
        <!-- Row 1: Gender Distribution and Leadership Comparison -->
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-6 ">
            <!-- <ChartCard title="Leadership Comparison" description="Comparison between Male and Female leadership ratings"
              :labels="['남성 (Male)', '여성 (Female)']" title_z="Leadership Category" title_y="Average Score"
              :chartType="'pie'" /> -->
            <ChartCard canvasId="leadershipChart" title="남성과 여성의 성장률 비교"
              description="본 그래프는 남성과 여성 참가자들의 리더십 프로그램 전후 성장률을 비교하여 성별에 따른 리더십 향상 정도를 시각화한 것입니다."
              :labels="leadershipLabels" :datasets="computedDatasets" title_z="Leadership Category"
              title_y="Average Score" :chartType="'bar'" />


          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-6">
            <ChartCard canvasId="demographicChart-age" title="결혼 여부에 따른 성장률 비교"
              description="해당 그래프는 미혼과 기혼 참가자 간의 성장률 차이를 분석합니다. 가정이 있는 사람들이 리더십 성장에서 더 높은 성과를 보이는지 여부를 확인할 수 있습니다."
              :labels="demographicLabels.marital" :datasets="demographicDatasets.marital" title_z="end this life"
              title_y="end" :chartType="'bar'" />




          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-6 ">
            <ChartCard_radar title="회사 내 성장률 vs 전체 평균 성장률 비교"
              description="본 그래프는 특정 회사의 참가자들이 리더십 프로그램을 통해 성장한 정도를 전체 평균과 비교하여 나타낸 것입니다. 특정 기업이 다른 기업들과 비교했을 때 얼마나 효과적인 성장을 보였는지를 확인할 수 있습니다."
              :labels="['Selflead Behavior', 'Selflead Natural', 'Selflead Constructive', 'Lifestyle']" :datasets="[
                {
                  label: 'Pre Survey',
                  data: [2.5, 3.0, 2.8, 3.2],
                  backgroundColor: 'rgba(54, 162, 235, 0.2)',
                  borderColor: 'rgba(54, 162, 235, 1)',
                  borderWidth: 2
                },
                {
                  label: 'Post Survey',
                  data: [3.8, 4.2, 3.9, 4.6],
                  backgroundColor: 'rgba(255, 99, 132, 0.2)',
                  borderColor: 'rgba(255, 99, 132, 1)',
                  borderWidth: 2
                }
              ]" />

          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-6">

            <ChartCard canvasId="demographicChart-age" title="연봉과 성장률 간의 관계 분석"
              description="해당 그래프는 참가자의 연봉 수준과 리더십 프로그램 이후 성장률 간의 관계를 나타냅니다. 연봉이 높은 집단과 낮은 집단의 성장 패턴을 비교할 수 있습니다."
              :labels="demographicLabels.salary" :datasets="demographicDatasets.age" title_z="end this life"
              title_y="end" :chartType="'bar'" />


          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12 sm:col-span-12 lg:col-span-12 ">
            <HeatmapChart title="라이프스타일 요인과 성장률의 관계"
              description="수면, 운동, 식습관, 명상, 일과 삶의 균형과 같은 라이프스타일 요인이 리더십 성장률에 미치는 영향을 분석한 그래프입니다. 건강한 생활 습관이 얼마나 성과에 기여하는지 확인할 수 있습니다."
              :lifestyleLabels="['Sleep', 'Exercise', 'Meditation', 'Diet', 'Balance']" :scores="[1, 2, 3, 4, 5]"
              :improvementData="[
                [1.2, 1.5, 2.1, 1.8, 1.9],
                [2.4, 2.7, 3.0, 2.9, 2.5],
                [3.5, 3.2, 3.8, 3.4, 3.9],
                [4.1, 4.3, 4.7, 4.5, 4.2],
                [5.0, 5.2, 5.5, 5.1, 5.3]
              ]" />
          </div>

        </div>
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-12 md:col-span-12  lg:col-span-12 ">
            <ChartCard canvasId="demographicChart-age" title="학력과 리더십 성장률 비교"
              description=" 해당 그래프는 참가자의 최종 학력(고졸, 전문대졸, 대졸, 대학원 졸업 등)에 따른 리더십 성장률의 차이를 나타냅니다. 학력이 높은 집단과 낮은 집단의 성장률 차이를 분석할 수 있습니다."
              :labels="demographicLabels.education" :datasets="demographicDatasets.education" title_z="end this life"
              title_y="end" :chartType="'bar'" />

          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-12 md:col-span-12  lg:col-span-12 ">


          </div>

        </div>
        <!-- Row 2: Age Distribution and Age Improvement Comparison -->


        <!-- Row 3: Job Distribution and Job Salary Comparison -->


      </div>
    </main>
  </div>

</template>
<!-- <section class="mt-10" v-for="category in demographicCategories" :key="category">
  <h2 class="text-xl font-semibold text-gray-700 mb-2">
    {{ getDisplayCategory(category) }} vs Survey Improvement
  </h2>
  <div class="bg-white p-4 rounded shadow">
    <canvas :id="`${category}Chart`"></canvas>
  </div>
</section> -->

<script setup>
import { ref, reactive, onMounted, nextTick, computed, inject } from 'vue';
import { Chart, registerables } from 'chart.js';

import DashCard from '../components/ui/DashCard.vue';

Chart.register(...registerables);

import ChartCard_pie from '../components/ui/ChartCard_pie.vue';
import ChartCard_bar from '../components/ui/ChartCard_bar.vue';
import ChartCard from '../components/ui/ChartCard.vue';
import ChartCard_radar from '../components/ui/ChartCard_radar.vue';
import HeatmapChart from '../components/ui/HeatmapChart.vue';
const loading = ref(true);
const errorMessage = ref('');
const leadershipData = ref([]);
const demographicData = reactive({
  age: [],
  salary: [],
  education: [],
  marital: []
});



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
    console.log("✅ leadership API Responses:", leadershipData);
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
    console.log("✅ Demographic API Responses:", demographicData);
  } catch (error) {
    console.error(error);
    errorMessage.value = "Error fetching demographic data.";
  }
};
// Create a computed property that transforms raw leadershipData into Chart.js data.
const leadershipChartData = computed(() => {
  if (!leadershipData.value || leadershipData.value.length === 0) {
    return { labels: [], datasets: [] };
  }
  const labels = leadershipData.value.map(entry => entry.category);
  const maleData = leadershipData.value.map(entry => entry['남성']);
  const femaleData = leadershipData.value.map(entry => entry['여성']);
  return {
    labels,
    datasets: [
      { label: '남성 (Male)', data: maleData, backgroundColor: '#4F46E5' },
      { label: '여성 (Female)', data: femaleData, backgroundColor: '#A78BFA' }
    ]
  };
});
const leadershipLabels = computed(() => leadershipChartData.value?.labels ?? []);
const computedDatasets = computed(() => {
  if (!leadershipChartData.value || !leadershipChartData.value.datasets) return [];
  return leadershipChartData.value.datasets.map(dataset => ({
    ...dataset,
    data: [...dataset.data] // ✅ Unwrap Proxy safely
  }));
});


const demographicChartData = computed(() => {
  const result = {};
  demographicCategories.forEach(category => {
    const data = demographicData[category];
    if (data && data.length > 0) {
      // Construct the labels using the pattern: `${category}_group`
      // (e.g. for "age", the key should be "age_group")
      result[category] = {
        labels: data.map(entry => entry[`${category}_group`]),
        datasets: [
          {
            label: 'Pre Survey',
            data: data.map(entry => entry.pre),
            backgroundColor: '#4F46E5'
          },
          {
            label: 'Post Survey',
            data: data.map(entry => entry.post),
            backgroundColor: '#A78BFA'
          }
        ]
      };
    } else {
      result[category] = null;
    }
  });
  return result;
});

// A computed property to extract labels for each demographic category.
const demographicLabels = computed(() => {
  const result = {};
  demographicCategories.forEach(category => {
    result[category] =
      (demographicChartData.value[category] && demographicChartData.value[category].labels) || [];
  });
  return result;
});

// A computed property to extract the datasets for each demographic category,
// unwrapping any Vue Proxy objects.
const demographicDatasets = computed(() => {
  const result = {};
  demographicCategories.forEach(category => {
    if (demographicChartData.value[category] && demographicChartData.value[category].datasets) {
      result[category] = demographicChartData.value[category].datasets.map(dataset => ({
        ...dataset,
        data: [...dataset.data] // Unwrap Proxy safely.
      }));
    } else {
      result[category] = [];
    }
  });
  return result;
});

const isPrinting = inject("isPrinting");
const printDashboard = () => {
  console.log("🔄 Preparing charts for printing...");
  isPrinting.value = true;
  document.body.style.width = "1000px";
  document.body.style.height = "auto";

  window.dispatchEvent(new Event("resize")); // ✅ Force resize event

  setTimeout(() => {
    console.log("🖨 Printing...");
    window.print();
  }, 500); // ✅ Delay ensures chart resize before printing
};



// On component mount, fetch backend data and render charts
onMounted(async () => {
  // Fetch all the necessary data
  await fetchLeadershipData();
  await fetchDemographicData();
  // Use nextTick to wait until the DOM is updated (all canvas elements are rendered)
  nextTick(() => {
    loading.value = false;
  });
});
</script>

<style scoped>
/* Optional styling adjustments */


/* Print styles: force white background and hide print-only elements (like the print button) */
@media print {

  body {
    width: 1100px;
    height: auto;
    /* Prevents sudden width changes */
  }


}
</style>