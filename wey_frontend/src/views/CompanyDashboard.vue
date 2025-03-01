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
      <h1 class="text-2xl text-bold pb-3 print:text-black mb-6 print:mb-6">{{ companyStats.name }}</h1>

      <!-- <router-view /> -->
      <div class="grid grid-cols-12 gap-5 pb-5 print:hidden">
        <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-4 ">
          <DashCard title="프로그램 참여 지원 수" :description="companyStats.user_count + '명'" percentage="26%"
            content="증가(지난달 대비)" />
        </div>
        <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-4  ">
          <DashCard title="평균 성장률" :description="companyStats.average_growth + '%'" percentage="14%"
            content="증가(지난달 대비)" />
        </div>
        <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-4 ">
          <DashCard title="선택 프로그램" :description="companyStats.course_type" percentage="" content="" />
        </div>
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
          <div class="col-span-12 sm:col-span-6 md:col-span-5  lg:col-span-5 print:col-span-5">
            <ChartCard :title="'남성과 여성 ' + companyStats.course_type + ' 분포 비교'"
              :description="'이 파이 그래프는 조직 내 남성과 여성의 ' + companyStats.course_type + ' 비율을 비교하여, 기업·공공기관·산업별 ' + companyStats.course_type + ' 분포를 시각적으로 나타냅니다.'"
              :labels="genderLabels" :datasets="genderDatasets" title_z="Leadership Category" title_y="Average Score"
              :chartType="'pie'" />

            <!--  -->


          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-7 lg:col-span-7 print:col-span-7">
            <ChartCard canvasId="leadershipChart" :title="'남성과 여성의 ' + companyStats.course_type + ' 비교'"
              description="본 그래프는 교육과정에 따른 질문 범주별 남성과 여성의 평균 점수를 비교합니다." :labels="leadershipLabels"
              :datasets="computedDatasets" title_z="Leadership Category" title_y="Average Score" :chartType="'bar'" />
          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-6 md:col-span-7  lg:col-span-7 print:col-span-7">
            <ChartCard canvasId="demographicChart-age" :title="'연봉과 ' + companyStats.course_type + ' 간의 관계 분석'"
              :description="'본 그래프는 참가자의 연봉 수준과 ' + companyStats.course_type + ' 프로그램 이후 성장률 간의 관계를 나타냅니다.'"
              :labels="demographicLabels.salary" :datasets="demographicDatasets.salary" title_z="end this life"
              title_y="end" :chartType="'bar'" />

          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-5 lg:col-span-5 print:col-span-5">
            <ChartCard_radar title="회사 내 성장률 vs 전체 평균 성장률 비교"
              :description="'본 그래프는 특정 회사 참가자의 ' + companyStats.course_type + ' 성장률을 전체 평균과 비교하여 기업 간 성장 차이를 확인합니다.'"
              :labels="prepostChartLabel" :datasets="prepostChartData" />



          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-6 ">
            <ChartCard canvasId="demographicChart-age" :title="'학력과' + companyStats.course_type + '성장률 비교'"
              :description="'본 그래프는 참가자의 학력 수준(고졸, 대졸 등)에 따른' + companyStats.course_type + '성장률 차이를 분석합니다.'"
              :labels="demographicLabels.education" :datasets="demographicDatasets.education" title_z="end this life"
              title_y="end" :chartType="'bar'" />

          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-6">
            <ChartCard canvasId="demographicChart-age" :title="'결혼 여부에 따른 ' + companyStats.course_type + ' 비교'"
              :description="'본 그래프는 미혼과 기혼 참가자의 ' + companyStats.course_type + ' 성장 차이를 분석하여 결혼이 성장에 미치는 영향을 확인합니다.'"
              :labels="demographicLabels.marital" :datasets="demographicDatasets.marital" title_z="end this life"
              title_y="end" :chartType="'bar'" />
          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-6 ">
            <ChartCard canvasId="demographicChart-age" :title="'직무 분야와 ' + companyStats.course_type + ' 성장률 비교'"
              :description="'이 그래프는 참가자의 직무 분야(IT, 금융, 교육 등)에 따른 ' + companyStats.course_type + ' 성장률 차이를 분석합니다.'"
              :labels="demographicLabels.job_field" :datasets="demographicDatasets.job_field" title_z="end this life"
              title_y="end" :chartType="'bar'" />

          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-6">
            <ChartCard canvasId="demographicChart-age" :title="'고용 형태와 ' + companyStats.course_type + ' 성장률 비교'"
              :description="'이 그래프는 참가자의 고용 형태(정규직, 계약직, 프리랜서 등)에 따른 ' + companyStats.course_type + ' 성장 차이를 분석합니다.'"
              :labels="demographicLabels.employment_type" :datasets="demographicDatasets.employment_type"
              title_z="end this life" title_y="end" :chartType="'bar'" />
          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-6 ">
            <ChartCard canvasId="demographicChart-age" :title="'근속 연수와 ' + companyStats.course_type + ' 성장률 비교'"
              :description="'이 그래프는 참가자의 근속 연수(재직 기간)에 따른 ' + companyStats.course_type + ' 성장률을 분석합니다.'"
              :labels="demographicLabels.tenure" :datasets="demographicDatasets.tenure" title_z="end this life"
              title_y="end" :chartType="'bar'" />

          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-6">
            <ChartCard canvasId="demographicChart-age" :title="'직급과 ' + companyStats.course_type + ' 성장률 비교'"
              :description="'이 그래프는 참가자의 직급(사원, 대리, 팀장, 임원 등)에 따른 ' + companyStats.course_type + ' 성장률 차이를 분석합니다.'"
              :labels="demographicLabels.position" :datasets="demographicDatasets.position" title_z="end this life"
              title_y="end" :chartType="'bar'" />
          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 print:pb-24">
          <div class="col-span-12 sm:col-span-12 lg:col-span-12 ">

            <HeatmapChart title="라이프스타일 요인과 성장률의 관계"
              :description="'라이프스타일과 워크라이프 밸런스와 같은 요소가 ' + companyStats.course_type + ' 성장률에 미치는 영향을 분석합니다.'"
              :lifestyleLabels="['여유', '에너지', '스타일', '패션', '신제품', '취미', '거주', '근무', '노후', '변화', '심플', '전통', '자기개발', '건강', '운동']"
              :scores="[1, 2, 3, 4, 5]" :improvementData="transformedHeatmapData" />
          </div>

        </div>


        <!-- Large Text Box for Admin Explanation -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12">
            <h2 class="text-xl font-semibold text-gray-100 print:text-black">리포트 설명</h2>
            <textarea v-model="adminExplanation"
              class="w-full h-48 p-4 border border-gray-600 rounded-md text-white print:text-black print:border-black bg-transparent"
              placeholder="차트에 대한 설명을 입력하세요..."></textarea>
            <button @click="saveExplanation"
              class="right-4 bottom-4 bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 print:hidden">
              저장
            </button>
          </div>
        </div>

        <!-- Row 2: Age Distribution and Age Improvement Comparison -->


        <!-- Row 3: Job Distribution and Job Salary Comparison -->

        <div class="print:flex flex-col items-end justify-end p-4 space-y-2 hidden">

          <a href="https://yourwebsite.com" target="_blank">
            <img src="/Images/Logo.png" alt="Logo" class="w-[13rem] h-auto  ">
          </a>
          <div class="text-black">https://rebootcommons.com</div>
        </div>
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
import { ref, reactive, onMounted, nextTick, computed, inject, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';
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
const heatmapData = ref(null);
const company_vs_all = ref(null);
const genderDistributionData = ref([]);
const adminExplanation = ref("");
const demographicData = reactive({
  gender: [],
  age: [],
  salary: [],
  education: [],
  marital: []
});
const companyStats = ref({
  user_count: 0,
  average_growth: 0,
  course_type: '정보 없음',
  company_name: '정보 없음'
});
const categoryNameMapping = {




  "demographic": "인구통계학",
  "lifestlyes": "라이프",
  "entrepreneur_risk": "위험감수성",
  "entrepreneur_proact": "진취성",
  "entrepreneur_innov": "혁신성",
  "org_normative": "규범적몰입",
  "org_continuance": "지속적몰입",
  "org_affective": "정서적몰입",
  "ppc_resilience": "회복탄력성",
  "ppc_hope": "희망",
  "ppc_optimism": "낙관성",
  "ppc_efficacy": "자기효능감",
  "selflead_behavior": "행동중심전략",
  "selflead_natural": "자연적보상",
  "selflead_constructive": "건설적사고",
};

const route = useRoute()
// Adjust these categories as needed (they should match your backend endpoint names)
const demographicCategories = ['gender', 'age', 'salary', 'education', 'marital', 'job_field', 'employment_type', 'position', 'tenure'];


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
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/companies/${companyId}/gender-leadership/`, {
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

const fetchGenderDistribution = async () => {
  try {
    const companyId = window.location.pathname.split("/").pop();
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      errorMessage.value = "Authentication token missing.";
      return;
    }

    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/companies/${companyId}/gender-counts/`, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch gender distribution. Status: ${response.status}`);
    }

    const json = await response.json();
    console.log("✅ Gender Distribution Data:", json); // Ensure correct response

    // Assign data to ref
    genderDistributionData.value = json.data;
  } catch (error) {
    console.error("Error fetching gender distribution:", error);
    errorMessage.value = "Error fetching gender distribution.";
  }
};


const fetchCompanyStatistics = async () => {
  try {
    // Extract company ID from URL (adjust this if needed)
    const companyId = window.location.pathname.split('/').pop();
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      errorMessage.value = 'Authentication token missing.';
      loading.value = false;
      return;
    }
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/companies/${companyId}/statistics/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch company statistics');
    }
    companyStats.value = await response.json();
    console.log("✅ Company Statistics:", companyStats.value);
  } catch (err) {
    console.error(err);
    errorMessage.value = 'Error fetching company statistics.';
  }
};

// Fetch demographic data for each category from the backend
const fetchDemographicData = async () => {
  const userId = route.params.id;
  console.log(userId);
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
          `${import.meta.env.VITE_API_URL}/api/dashboard/${companyId}/demographic-improvement/${category}/`,
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

// Function to fetch the current explanation from the backend
const fetchExplanation = async () => {
  const companyId = window.location.pathname.split('/').pop();
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/companies/${companyId}/explanation/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
    });

    adminExplanation.value = response.data.explanation_text;
    console.log("Fetched explanation:", adminExplanation.value);
  } catch (error) {
    console.error("Error fetching explanation:", error);
  }
};

// Function to save (update) the explanation
const saveExplanation = async () => {
  const companyId = window.location.pathname.split('/').pop();
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_URL}/api/companies/${companyId}/explanation/`,
      { explanation_text: adminExplanation.value },
      { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
    );
    console.log("Explanation saved successfully:", response.data);
  } catch (error) {
    console.error("Error saving explanation:", error);
  }
};

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
            label: '사전 점수',
            data: data.map(entry => entry.pre),
            backgroundColor: '#4F46E5'
          },
          {
            label: '사후 점수',
            data: data.map(entry => entry.post),
            backgroundColor: '#A78BFA'
            // backgroundColor: "rgba(182, 91, 252, 0.2)",
            // borderColor: "rgba(182, 91, 252, 1)",
            // borderWidth: 2,
            // backgroundColor: '#A78BFA'
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
// Create a computed property that transforms raw leadershipData into Chart.js data.
const leadershipChartData = computed(() => {
  if (!leadershipData.value || leadershipData.value.length === 0) {
    return { labels: [], datasets: [] };
  }
  const labels = leadershipData.value.map(entry => categoryNameMapping[entry.category] || entry.category);
  const maleData = leadershipData.value.map(entry => entry['남성']);
  const femaleData = leadershipData.value.map(entry => entry['여성']);
  return {
    labels,
    datasets: [
      { label: '남성', data: maleData, backgroundColor: '#4F46E5' },
      { label: '여성', data: femaleData, backgroundColor: '#A78BFA' }
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

// Fetch heatmap data from the API.
const fetchHeatmapData = async () => {
  try {
    const companyId = window.location.pathname.split("/").pop();
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      errorMessage.value = "Authentication token missing.";
      return;
    }
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/api/dashboard/${companyId}/lifestyle-performance-growth/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );
    heatmapData.value = response.data;
    console.log("✅ Raw heatmap data:", heatmapData.value);
  } catch (err) {
    console.error("Error fetching heatmap data:", err);
  }
};

const fetchRadarData = async () => {
  try {
    const companyId = window.location.pathname.split("/").pop();
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      errorMessage.value = "Authentication token missing.";
      return;
    }
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/api/dashboard/${companyId}/growth-comparison/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );
    company_vs_all.value = response.data;
    console.log("✅ Raw Radar data:", company_vs_all.value);
  } catch (err) {
    console.error("Error fetching radar data:", err);
  }
};

// ADDED CODE: Create computed properties for the radar chart data to be used by <ChartCard_radar>
const prepostChartLabel = computed(() => {
  // Use the data from userGrowthData (fetched from the user-growth-comparison endpoint)
  // return company_vs_all.value?.categories || [];
  return company_vs_all.value?.categories.map(category => {
    console.log(category)
    // console.log(category.name)
    return categoryNameMapping[category] || category;
  });
});

const prepostChartData = computed(() => {

  if (!company_vs_all.value) return [];
  console.log("this user", company_vs_all.value.company_scores);
  console.log("all user", company_vs_all.value.industry_scores);
  return [
    {
      label: "기업 점수",
      data: company_vs_all.value.company_scores || [],
      backgroundColor: "rgba(193, 99, 255, 0.3)",
      borderColor: "rgba(193, 99, 255, 1)",
      borderWidth: 2,
    },
    {
      label: "산업 평균 점수",
      data: company_vs_all.value.industry_scores || [],
      backgroundColor: "rgba(54, 162, 235, 0.3)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 2,
    }
  ];

});

const genderLabels = computed(() => {
  return genderDistributionData.value
    ? Object.keys(genderDistributionData.value) // ["남성", "여성"]
    : [];
});

const genderDatasets = computed(() => {
  return genderDistributionData.value
    ? [
      {
        label: "Gender Distribution",
        data: Object.values(genderDistributionData.value), // [8, 7]
        backgroundColor: ["#4F46E5", "#A78BFA"]
      }
    ]
    : [];
});


// Define the mapping between the API question prefix and the full Korean label.
const lifestyleMappings = [
  { key: "라이프스타일: 1", label: "삶의 여유를 가지고 생활하는 편이다." },
  { key: "라이프스타일: 2", label: "하고 싶은 일을 할 충분한 에너지가 있다." },
  { key: "라이프스타일: 3", label: "나만의 스타일이 있다는 이야기를 자주 듣는다." },
  { key: "라이프스타일: 4", label: "새로운 패션이나 유행에 민감하다." },
  { key: "라이프스타일: 5", label: "신제품이 출시되면 남보다 빨리 구매하는 편이다." },
  { key: "라이프스타일: 6", label: "취미활동을 위한 모임이나 동호회 활동에 정기적으로 참여한다." },
  { key: "라이프스타일: 7", label: "이사를 하지 않고 한 곳에서 오래 사는 것이 좋다." },
  { key: "라이프스타일: 8", label: "나는 제한된 근무를 선호한다." },
  { key: "라이프스타일: 9", label: "노후를 대비하여 계획을 세우고 있다." },
  { key: "라이프스타일: 10", label: "다양한 변화가 있는 생활을 좋아한다." },
  { key: "라이프스타일: 11", label: "단순한 삶(심플·미니멀 라이프)을 살고 싶다." },
  { key: "라이프스타일: 12", label: "새로운 것을 추구하기보다 전부터 해 오던 방식을 따르는 편이다." },
  { key: "라이프스타일: 13", label: "자기개발을 위한 노력을 계속하는 편이다." },
  { key: "라이프스타일: 14", label: "나의 건강과 노후에 관심이 많다." },
  { key: "라이프스타일: 15", label: "건강을 위해 주기적인 운동을 하며 정기검진을 받고 있다." }
];

// Compute the transformed heatmap data (averaged to one decimal place).
const transformedHeatmapData = computed(() => {
  // Extract only the keys from the mapping.
  const keys = lifestyleMappings.map(mapping => mapping.key);

  // Initialize a matrix with 5 rows (for ratings 1-5) and as many columns as there are keys.
  const matrix = Array.from({ length: 5 }, () =>
    Array.from({ length: keys.length }, () => [])
  );

  if (!heatmapData.value || !heatmapData.value.data) return [];

  // Loop over each data item and place the growth values into the correct cell.
  heatmapData.value.data.forEach(item => {
    keys.forEach((key, colIndex) => {
      if (item.question.startsWith(key)) {
        const rowIndex = item.rating - 1;
        if (rowIndex >= 0 && rowIndex < 5) {
          matrix[rowIndex][colIndex].push(item.growth);
        }
      }
    });
  });

  // Compute the average for each cell and show one decimal place.
  const result = matrix.map(row =>
    row.map(cell => {
      if (cell.length === 0) return 0;
      const sum = cell.reduce((acc, val) => acc + val, 0);
      return Number((sum / cell.length).toFixed(1));
    })
  );
  console.log("Transformed heatmap data (2D array):", result);
  return result;
});

const revertBodyStyles = () => {
  console.log("🔙 Reverting body styles after print...");
  document.body.style.width = "";
  document.body.style.height = "";
  isPrinting.value = false;
};


const isPrinting = inject("isPrinting");
const printDashboard = () => {
  console.log("🔄 Preparing charts for printing...");
  isPrinting.value = true;
  document.body.style.width = "1000px";
  document.body.style.height = "auto";
  window.dispatchEvent(new Event("resize"));
  window.dispatchEvent(new Event("chartBeforePrint"));
  setTimeout(() => {
    console.log("🖨 Printing...");
    window.print();
    window.dispatchEvent(new Event("chartAfterPrint"));
  }, 500);
};



// On component mount, fetch backend data and render charts
onMounted(async () => {
  // Fetch all the necessary data
  await fetchLeadershipData();
  await fetchDemographicData();
  await fetchHeatmapData();
  await fetchRadarData();
  await fetchCompanyStatistics();
  await fetchGenderDistribution();
  await fetchExplanation();
  window.addEventListener("chartAfterPrint", revertBodyStyles);
  // Use nextTick to wait until the DOM is updated (all canvas elements are rendered)
  nextTick(() => {
    loading.value = false;
  });
});

onUnmounted(() => {
  window.removeEventListener("chartAfterPrint", revertBodyStyles);
});
</script>

<style scoped>
/* Optional styling adjustments */


/* Print styles: force white background and hide print-only elements (like the print button) */
/* @media print {

  body {
    width: 1100px;
    height: auto;
  
  }


} */

@media print {

  /* Ensure the body takes the full available width, with no margin/padding */
  body {
    width: 100%;
    margin: 0;
    padding: 0;
  }

  /* Force your main container (or grid) to use a fixed width that fits on a printed page */
  .container,
  .flex-1 {
    width: 100%;
    max-width: 100%;
    /* or a value like 800px if you prefer a fixed width */
  }

  /* Prevent charts and other blocks from splitting between pages */
  .chart-container,
  .print-section,
  .rounded-lg {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Optionally, force a page break after major sections if needed */
  .page-break {
    page-break-after: always;
    break-after: page;
  }

  /* Adjust grid layout to use 100% width on print */
  .grid-cols-12 {
    grid-template-columns: repeat(12, 1fr);
  }


}
</style>