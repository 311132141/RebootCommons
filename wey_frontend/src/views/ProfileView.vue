<template>
  <div class="flex h-screen" v-if="!loading">
    <main class="flex-1 p-6 ">
      <div class="flex items-center justify-between mb-6 print:hidden">
        <div class="flex items-center space-x-2 text-gray-400 ">
          <span>Dashboard</span>
          <span>></span>
          <span>User page</span>
        </div>
        <div class="flex items-center space-x-4 ">
          <button @click="printDashboard"
            class=" bg-gray-800 p-2 rounded-md text-white px-4 py-2 rounded hover:bg-blue-600 print:hidden">
            리포트 작성하기
          </button>
        </div>
      </div>
      <h1 class="text-2xl text-bold pb-3 print:text-black mb-6 print:mb-6">{{ user.name }}의 데시보드</h1>

      <div class="space-y-6">
        <!-- <div class="grid grid-cols-12 gap-5 ">

        </div>

        <div class="grid grid-cols-12 gap-5 ">

        </div> -->

        <!-- Loop through each category and render a radar chart -->
        <div class="grid grid-cols-12 gap-5 ">
          <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-7 print:col-span-7 ">
            <div
              class="shadow p-4 rounded-border border border-gray-600 rounded-lg max-h-120 h-full items-stretch relative">
              <div class="ml-8">
                <h3 class="text-4xl font-bold text-white print:text-black">{{ user.name }}</h3>
                <ul class="mt-4 text-white print:text-black">
                  <li><strong>Email:</strong> {{ user.email }}</li>
                  <li><strong>성별:</strong> {{ user.demographics.gender }}</li>
                  <li><strong>연령:</strong> {{ user.demographics.age }}</li>
                  <li><strong>결혼 여부:</strong> {{ user.demographics.marital_status }}</li>
                  <li><strong>학력:</strong> {{ user.demographics.education }}</li>
                  <li><strong>소득 수준:</strong> {{ user.demographics.income }}</li>
                </ul>
                <!-- Selected Program -->
                <h2 class="text-xl font-semibold mt-6 text-gray-100 print:text-black">
                  선택한 프로그램:
                </h2>
                <div class="print:text-black">{{ user.demographics.selected_program }}</div>
              </div>
            </div>
          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-5 print:col-span-5">
            <ChartCard_radar title="개인 & 전체 프로그램 평균 성장률 비교" description="본 그래프는 개인의 성장률을 전체 프로그램 평균과 비교한 결과를 보여줍니다."
              :labels="UserVsAllLabel" :datasets="UserVsAllDataset" />
          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-5 print:col-span-5">
            <ChartCard_radar :title="`${user.demographics.selected_program} - 성장률 (전/후) 비교`"
              :description="`본 레이더 차트는 ${user.demographics.selected_program} 수강 전후의 성장률 변화를 항목별로 보여줍니다.`"
              :labels="prepostChartLabel" :datasets="prepostChartData" />

          </div>
          <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-7 print:col-span-7">
            <ChartCard :title="`${user.demographics.selected_program} - 성장률 (전/후) 비교`"
              :description="`본 막대 차트는 ${user.demographics.selected_program} 수강 전후의 성장률 변화를 항목별로 보여줍니다.`"
              :labels="prepostChartLabel" :datasets="prepostChartData" :chartType="'bar'" />
          </div>
          <div v-for="(radar, index) in radarDataPerCategory" :key="index"
            class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-4 print:col-span-4">
            <ChartCard_radar :title="`${radar.categoryName} - 성장률 (전/후) 비교`"
              :description="`본 그래프는 ${radar.categoryName} 내 전후 성장률 변화를 비교한 결과를 나타냅니다.`" :labels="radar.labels"
              :datasets="radar.datasets" />
          </div>
        </div>
        <div class="grid grid-cols-12 gap-5 pb-5 ">
          <div class="col-span-12 sm:col-span-12 lg:col-span-12 ">
            <HeatmapChart title="라이프스타일 요인과 성장률의 관계"
              description="수면, 운동, 식습관, 명상, 워크라이프 밸런스와 같은 요소가 리더십 성장률에 미치는 영향을 분석합니다. 건강한 생활 습관이 얼마나 성과에 기여하는지 확인할 수 있습니다."
              :lifestyleLabels="['여유', '에너지', '스타일', '패션', '신제품', '취미', '거주', '근무', '노후', '변화', '심플', '전통', '자기개발', '건강', '운동']"
              :scores="[1, 2, 3, 4, 5]" :improvementData="transformedHeatmapData" />
          </div>

        </div>
        <!-- Large Text Box for Admin Explanation -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12">
            <h2 class="text-xl font-semibold text-gray-100 print:text-black">리포트 설명</h2>
            <textarea v-model="adminExplanation"
              class="w-full h-48 p-4 border border-gray-600 rounded-md  text-white print:text-black print:border-black bg-transparent"
              placeholder="차트에 대한 설명을 입력하세요..."></textarea>
            <button
              class=" right-4 bottom-4 bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 print:hidden">
              저장
            </button>

          </div>
        </div>
      </div>



      <div class="print:flex flex-col items-end justify-end p-4 space-y-2 hidden">

        <a href="https://yourwebsite.com" target="_blank">
          <img src="/Images/Logo.png" alt="Logo" class="w-[13rem] h-auto ">
        </a>
        <div class="text-black">https://rebootcommons.com</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed, inject, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
import "chartjs-chart-matrix";

import DashCard from '../components/ui/DashCard.vue';
import ChartCard_pie from '../components/ui/ChartCard_pie.vue';
import ChartCard_bar from '../components/ui/ChartCard_bar.vue';
import ChartCard from '../components/ui/ChartCard.vue';
import ChartCard_radar from '../components/ui/ChartCard_radar.vue';
import HeatmapChart from '../components/ui/HeatmapChart.vue';

Chart.register(...registerables);

// Reactive state variables
const route = useRoute();
const loading = ref(true);
const errorMessage = ref('');
const user = ref({
  name: "",
  email: "",
  avatar: null,
  demographics: {}
});
const leadershipData = ref([]);
const heatmapData = ref(null);
const company_vs_all = ref(null);
const demographicData = reactive({
  age: [],
  salary: [],
  education: [],
  marital: []
});
const questionRatings = ref([]);
const questionGrowthData = ref({ categories: [] });

// Reactive variables for radar chart data
const UserVsAllData = ref(null);
const prePostRadarData = ref(null);
const questionNameMapping = {
  // 기업가정신(위험감수성)
  entrepreneur_risk: [
    "위험 감수하며 사업 추진",
    "실패 후 재도전 의지",
    "예상치 못한 문제 해결, 새로운 기회 발견",
    "적극적으로 기회에 뛰어들어 위험 감수",
    ["미래 이익 위해", "과감히 결정"],
  ],

  // 기업가정신(진취성)
  entrepreneur_proact: [
    "새로운 기회 즉시 실행",
    "창의적 아이디어 시도",
    "능동적으로 방안 모색",
    "기존 모델 개선점 탐색",
    "주도적 행동, 성취감 추구",
  ],

  // 기업가정신(혁신성)
  entrepreneur_innov: [
    "혁신 아이디어 적극 도입",
    "새로운 방식으로 문제 해결",
    "혁신 문화 조성에 노력",
    "위험 감수하고 혁신 투자",
    "시장 기회를 창출하는 혁신 접근",
  ],

  // 조직몰입(규범적몰입)
  org_normative: [
    "조직 규범·가치 충실 준수",
    "조직 기대에 부응하려 노력",
    "조직 규범 위배 시 죄책감",
    "조직에 받은 혜택 보답해야 한다고 느낌",
    "조직 명예·평판을 중요하게 여김",
  ],

  // 조직몰입(지속적몰입)
  org_continuance: [
    "조직 떠나면 손실 크다고 느낌",
    "현 조직을 떠나는 건 큰 위험",
    "경력·인맥 포기 어려움",
    "조직 유지가 경제적으로 유리",
    "다른 선택지보다 현재 조직이 낫다고 판단",
  ],

  // 조직몰입(정서적몰입)
  org_affective: [
    "조직에 대한 강한 소속감",
    "조직이 나에게 의미 있다고 생각",
    "조직 목표·가치를 내 것처럼 여김",
    "조직 성공이 곧 나의 성공",
    "조직 기여에 자부심을 느낌",
  ],

  // 긍정심리자본(회복탄력성)
  ppc_resilience: [
    "어려움 겪어도 금방 회복",
    "실패 후 빠른 재정비",
    "역경 속에서도 목표 향해 전진",
    "난관에 대처할 대안을 찾음",
    "시련을 성장 기회로 삼음",
  ],

  // 긍정심리자본(희망)
  ppc_hope: [
    "미래에 대한 긍정적 기대",
    "어려움 속에서도 희망 유지",
    "목표 달성 위한 구체적 계획",
    "장애 극복 가능하다고 믿음",
    "문제 해결에 적극적으로 노력",
  ],

  // 긍정심리자본(낙관성)
  ppc_optimism: [
    "내일이 더 나아질 거라 생각",
    "상황의 긍정적 면을 우선 봄",
    "실패에도 긍정적 교훈 발견",
    "미래가 밝을 것이라 기대",
    "일이 잘 풀릴 거라는 믿음",
  ],

  // 긍정심리자본(자기효능감)
  ppc_efficacy: [
    "어려운 과업도 해낼 수 있다는 확신",
    "새로운 도전에 자신감",
    "목표 달성 역량을 갖췄다고 생각",
    "문제 해결 능력이 충분하다고 느낌",
    "스스로 능력에 대한 믿음이 강함",
  ],

  // 자기리더십(행동지향전략)
  selflead_behavior: [
    "즉시 행동에 옮기는 편",
    "목표 달성 위해 행동 계획 수립",
    "스스로 실천력 점검",
    "자기 격려로 행동 유지",
    "직접 실행하며 학습",
  ],

  // 자기리더십(자연보상전략)
  selflead_natural: [
    "일에서 즐거움과 의미 찾음",
    "작은 성취에도 스스로 보상",
    "재미·보람으로 동기 부여",
    "업무 자체를 긍정적으로 바라봄",
    "환경을 즐길 수 있게 만들려 노력",
  ],

  // 자기리더십(건설적사고전략)
  selflead_constructive: [
    "긍정적 사고로 문제 접근",
    "부정적 감정 재구성·동기화",
    "목표 이미지를 구체적으로 상상",
    "자기 대화로 스스로 격려",
    "성공 시나리오에 집중",
  ],
};
const categoryNameMapping = {
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
  "selflead_behavior": "행동지향전략",
  "selflead_natural": "자연보상전략",
  "selflead_constructive": "건설적사고전략",
};
const extractQuestionText = (questionStr) => {
  // This regex removes everything up to and including the first occurrence of a number followed by a dot and space.
  return questionStr.replace(/.*\d+\.\s*/, '');
};

// Define demographic categories
const demographicCategories = ['age', 'salary', 'education', 'marital'];

// Helper function: map raw category key to display name
const getDisplayCategory = (cat) => {
  const mapping = {
    age: "Age Distribution",
    salary: "Salary Distribution",
    education: "Education Level",
    marital: "Marital Status",
  };
  return mapping[cat] || cat;
};

// Fetch user profile
const fetchUserProfile = async () => {
  const userId = route.params.id;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/profile/`);
    user.value = response.data;
    console.log(user.value)
  } catch (error) {
    console.error("Error fetching user profile:", error);
  }
};

// Fetch pre/post growth data
const fetchPrePostData = async () => {
  const userId = route.params.id;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/pre-post-comparison/`);
    if (!response.data.categories || response.data.categories.length === 0) {
      console.warn("No pre/post data returned");
      return;
    }
    prePostRadarData.value = response.data;
    console.log("prepost", prePostRadarData.value);
  } catch (error) {
    console.error("Error fetching pre/post data:", error);
  }
};

// Fetch user vs all growth data
const fetchUserVsAllGrowth = async () => {
  const userId = route.params.id;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/user-growth-comparison/`);
    if (!response.data.categories || response.data.categories.length === 0) {
      console.warn("No user vs all growth data returned");
      return;
    }
    UserVsAllData.value = response.data;
    console.log(UserVsAllData.value)
  } catch (error) {
    console.error("Error fetching user vs all growth data:", error);
  }
};

// Fetch heatmap data
const fetchHeatmapData = async () => {
  try {
    const companyId = window.location.pathname.split("/").pop();
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      errorMessage.value = "Authentication token missing.";
      return;
    }
    const response = await axios.get(
      `http://127.0.0.1:8000/api/dashboard/lifestyle-performance-growth/all/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );
    heatmapData.value = response.data;
    console.log("✅ Raw heatmap data:", heatmapData.value);
  } catch (error) {
    console.error("Error fetching heatmap data:", error);
  }
};

// Fetch question ratings data
const fetchQuestionRatings = async () => {
  const userId = route.params.id;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/question-pre-post-comparison/`);
    questionGrowthData.value = response.data;
    questionRatings.value = response.data.categories.flatMap(cat =>
      cat.questions.map(q => ({
        category: cat.name,
        question: q.question,
        pre_score: q.pre_score,
        post_score: q.post_score
      }))
    );
    console.log("questionGrowthData", questionGrowthData.value);

    console.log("what is this even", questionRatings.value);
    // Render manual question radar charts if needed
    // (Implementation omitted for brevity)
  } catch (error) {
    console.error("Error fetching question ratings data:", error);
  }
};



const radarDataPerCategory = computed(() => {
  if (!questionGrowthData.value || !questionGrowthData.value.categories) return [];
  return questionGrowthData.value.categories.map(category => {
    // Remap category name using the mapping, fallback to the original name if no match.
    const koreanCategoryName = categoryNameMapping[category.name] || category.name;
    const shortQuestions = questionNameMapping[category.name];
    return {
      categoryName: koreanCategoryName,
      labels: category.questions.map(q => extractQuestionText(q.question)),
      labels: category.questions.map((q, index) => {
        // If shortQuestions array exists and has an entry for this index, use it;
        // otherwise, fallback to extractQuestionText.
        if (shortQuestions && shortQuestions[index]) {
          return shortQuestions[index];
        } else {
          return extractQuestionText(q.question);
        }
      }),
      datasets: [
        {
          label: "사전 점수",
          data: category.questions.map(q => q.pre_score),
          backgroundColor: "rgba(193, 99, 255, 0.3)",
          borderColor: "rgba(193, 99, 255, 1)",
          borderWidth: 2,
        },
        {
          label: "사후 점수",
          data: category.questions.map(q => q.post_score),
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 2,
        }
      ]
    };
  });
});


// Computed properties for radar charts using prePostRadarData and userGrowthData
const prepostChartLabel = computed(() => {
  return prePostRadarData.value?.categories.map(category => {
    console.log(category)
    // console.log(category.name)
    return categoryNameMapping[category] || category;
  });
  // return prePostRadarData.value?.categories || [];
});
const prepostChartData = computed(() => {
  if (!prePostRadarData.value) return [];
  console.log("Pre Survey Scores:", prePostRadarData.value.pre_scores);
  console.log("Post Survey Scores:", prePostRadarData.value.post_scores);
  return [
    {
      label: "사전 점수",
      data: prePostRadarData.value.pre_scores || [],
      backgroundColor: "rgba(193, 99, 255, 0.3)",
      borderColor: "rgba(193, 99, 255, 1)",
      borderWidth: 2,
    },
    {
      label: "사후 점수",
      data: prePostRadarData.value.post_scores || [],
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 2,
    }
  ];
});

const UserVsAllLabel = computed(() => {
  return UserVsAllData.value?.categories.map(category => {
    console.log(category)
    // console.log(category.name)
    return categoryNameMapping[category] || category;
  });
});
const UserVsAllDataset = computed(() => {
  if (!UserVsAllData.value) return [];
  console.log("User Growth:", UserVsAllData.value.user_scores);
  console.log("All Users Growth:", UserVsAllData.value.all_users_scores);
  return [
    {
      label: "개별 성장률",
      data: UserVsAllData.value.user_scores || [],
      backgroundColor: "rgba(193, 99, 255, 0.3)",
      borderColor: "rgba(193, 99, 255, 1)",
      borderWidth: 2,
    },
    {
      label: "전체 사용자 성장률",
      data: UserVsAllData.value.all_users_scores || [],
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 2,
    }
  ];
});

// Mapping for heatmap data
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

// Compute transformed heatmap data as a 2D array (5 rows for ratings 1-5, columns per mapping)
const transformedHeatmapData = computed(() => {
  const keys = lifestyleMappings.map(mapping => mapping.key);
  const matrix = Array.from({ length: 5 }, () =>
    Array.from({ length: keys.length }, () => [])
  );
  if (!heatmapData.value || !heatmapData.value.data) return [];
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

onMounted(async () => {
  await fetchUserProfile();
  await fetchPrePostData();
  await fetchUserVsAllGrowth();
  await fetchHeatmapData();
  // await fetchRadarData();
  await fetchQuestionRatings();
  window.addEventListener("chartAfterPrint", revertBodyStyles);
  nextTick(() => {
    loading.value = false;
  });
});

onUnmounted(() => {
  window.removeEventListener("chartAfterPrint", revertBodyStyles);
});
</script>

<style scoped>
@media print {
  body {
    width: 1100px;
    height: auto;
  }
}
</style>