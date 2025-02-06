<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

import Skeleton from 'primevue/skeleton';
import { RouterLink, RouterView } from "vue-router";
import Card from 'primevue/card';
import Chart from 'primevue/chart';
import HeatmapChart from '../components/ui/HeatmapChart.vue';
import ChartCard from '../components/ui/ChartCard.vue';
import CardSmall from '../components/ui/CardSmall.vue';
import DashCard from '../components/ui/DashCard.vue';
import ChartCard_bar from '../components/ui/ChartCard_bar.vue';
// import Chart from 'primevue/chart';

// Example Chart Data and Options
const pieChartData = {
  labels: ['Electronics', 'Clothing', 'Accessories'],
  datasets: [
    {
      data: [300, 150, 200],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
    },
  ],
};

const pieChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
  },
};

const barChartData = {
  labels: ['January', 'February', 'March', 'April'],
  datasets: [
    {
      label: 'Sales',
      data: [50, 75, 100, 125],
      backgroundColor: '#36A2EB',
    },
  ],
};

const barChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
  },
};
// **1. 성별 분포**
// const genderDistributionData = {
//   labels: ['남성', '여성'],
//   datasets: [
//     {
//       data: [60, 40], // 예시 데이터: 남성 60%, 여성 40%
//       backgroundColor: ['#4F46E5', '#A78BFA'],
//     },
//   ],
// };
// Reactive state to store gender distribution data
const genderDistributionData = ref(null);

// Fetch gender distribution data from the backend
const fetchGenderDistributionData = async () => {
  try {
    const response = await axios.get('/api/graphs/gender-distribution/');
    genderDistributionData.value = response.data; // Populate the chart data
  } catch (error) {
    console.error('Error fetching gender distribution data:', error);
  }
};

// Fetch the data when the component mounts
onMounted(() => {
  fetchGenderDistributionData();
});
const genderDistributionOptions = {
  responsive: true,
  plugins: {
    legend: { display: true, position: 'top' },
  },
};

// Reactive state for chart data
const ageDistributionData = ref(null);

// Chart options (kept reusable for other charts)
const ageDistributionOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
  },
};

// Function to fetch age distribution data
const fetchAgeDistributionData = async () => {
  try {
    const response = await axios.get('/api/graphs/age-distribution/');
    ageDistributionData.value = response.data; // Populate the chart data
  } catch (error) {
    console.error('Error fetching age distribution data:', error);
  }
};

// Fetch data on component mount
onMounted(() => {
  fetchAgeDistributionData();
});
// **2. 프로그램 성과**
const programPerformanceData = {
  labels: ['비전하우스', '리더십', '기업가정신'],
  datasets: [
    {
      label: '참가율 (%)',
      data: [80, 90, 70], // 예시 데이터
      backgroundColor: ['#A78BFA', '#C4B5FD', '#DDD6FE'],
    },
    {
      label: '평균 성장률 (%)',
      data: [8.5, 10.5, 7.2], // 예시 데이터
      backgroundColor: ['#7C3AED', '#8B5CF6', '#A5B4FC'],
    },
  ],
};
const programPerformanceOptions = {
  responsive: true,
  plugins: {
    legend: { display: true, position: 'top' },
  },
};

// 3. **각 프로그램의 참가 비율**
const programParticipationChartData = {
  labels: ['리더십', '혁신', '기술'],
  datasets: [
    {
      data: [40, 30, 30], // 예시 데이터
      backgroundColor: ['#7C3AED', '#A78BFA', '#DDD6FE'],
    },
  ],
};
const programParticipationChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
  },
};


// 4. **프로그램별 참가자 수와 성장률 비교**
const programComparisonChartData = {
  labels: ['비전하우스', '리더십', '기업가정신'],
  datasets: [
    {
      label: '참가자 수',
      data: [120, 200, 150], // 예시 데이터
      backgroundColor: ['#A78BFA', '#C4B5FD', '#DDD6FE'],
    },
    {
      label: '평균 성장률 (%)',
      data: [10.2, 15.5, 12.3], // 예시 데이터
      backgroundColor: ['#7C3AED', '#8B5CF6', '#A5B4FC'],
    },
  ],
};
const programComparisonChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
  },
};
const programComparisonOptions = {
  responsive: true,
  plugins: {
    legend: { display: true, position: 'top' },
  },
};

// 5. **주요 성장 지표의 사전/사후 비교**
const beforeAfterChartData = {
  labels: ['행동중심전략', '리더십 점수', '혁신 지수'],
  datasets: [
    {
      label: '사전',
      data: [3.2, 4.1, 3.8], // 예시 데이터
      backgroundColor: '#DDD6FE',
    },
    {
      label: '사후',
      data: [4.1, 4.8, 4.5], // 예시 데이터
      backgroundColor: '#A78BFA',
    },
  ],
};
const beforeAfterChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
  },
};
</script>

<template>

  <div class="flex h-screen">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 text-white">
      <div class="p-4 font-bold text-lg">
        <router-link to="/" class="text-white">Dashboard</router-link>
      </div>
      <nav class="mt-4 space-y-2">
        <router-link to="/" class="block px-4 py-2 hover:bg-gray-700" active-class="bg-gray-700">
          Home
        </router-link>
        <router-link to="/analytics" class="block px-4 py-2 hover:bg-gray-700" active-class="bg-gray-700">
          Analytics
        </router-link>
        <router-link to="/settings" class="block px-4 py-2 hover:bg-gray-700" active-class="bg-gray-700">
          Settings
        </router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Navbar -->


      <!-- Dynamic Content -->
      <main class="flex-1 p-6 ">
        <div class="text-3xl text-bold pb-3">Overview</div>
        <!-- <router-view /> -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <DashCard />
          <DashCard />
          <DashCard />
          <DashCard />
        </div>
        <!-- <div class="pb-6 grid grid-cols-1 md:grid-cols-4 gap-6 ">
          <CardSmall title="Sales Data" description="150명" />
          <CardSmall title="Sales Data" description="140명" />
          <CardSmall title="Sales Data" description="150명" />
          <CardSmall title="Sales Data" description="150명" />
        </div> -->
        <div class="grid grid-cols-12 gap-5 pb-5">
          <div class="col-span-12 md:col-span-12 lg:col-span-5 ">
            <ChartCard title="성별 분포" description="이 그래프는 각 프로그램에 등록한 총 참가자 수와 평균 성장률을 시각화합니다." chartType="pie"
              :chartData="genderDistributionData" :chartOptions="genderDistributionOptions" />
          </div>
          <div class="col-span-12 md:col-span-12 lg:col-span-7 ">
            <ChartCard_bar title="User Age Distribution" description="이 그래프는 각 프로그램에 등록한 총 참가자 수와 평균 성장률을 시각화합니다."
              chartType="bar" :chartData="ageDistributionData" :chartOptions="ageDistributionOptions" />
          </div>

        </div>
        <div class="pb-6 grid grid-cols-1 md:grid-cols-3 gap-6 ">
          <!-- Example 1: Pie Chart -->
          <ChartCard title="성별 분포" description="이 그래프는 각 프로그램에 등록한 총 참가자 수와 평균 성장률을 시각화합니다." chartType="pie"
            :chartData="genderDistributionData" :chartOptions="genderDistributionOptions" />
          <!-- Example 2: Bar Chart -->
          <ChartCard title="User Age Distribution"
            description="This chart shows the distribution of users by age group." chartType="bar"
            :chartData="ageDistributionData" :chartOptions="ageDistributionOptions" class="col-span-2" />

        </div>
        <div class="text-3xl text-bold pb-3">프로그램 성과</div>
        <div class="pb-6 grid grid-cols-1 md:grid-cols-3 gap-6 ">
          <!-- Example 1: Pie Chart -->
          <ChartCard title="각 프로그램의 참가 비율" description="이 그래프는 각 프로그램에 등록한 총 참가자 수와 평균 성장률을 시각화합니다." chartType="bar"
            :chartData="programParticipationChartData" :chartOptions="programParticipationChartOptions"
            class="col-span-2" />
          <!-- Example 2: Bar Chart -->
          <!-- 3. 각 프로그램의 참가 비율 -->
          <ChartCard title="각 프로그램의 참가 비율" description="이 그래프는 각 프로그램에 등록한 총 참가자 수와 평균 성장률을 시각화합니다." chartType="pie"
            :chartData="programParticipationChartData" :chartOptions="programParticipationChartOptions" />
        </div>
        <div class="text-3xl text-bold pb-3">사전-사후 성장 분석</div>
        <div class="pb-6 grid grid-cols-1 md:grid-cols-2 gap-6 ">
          <!-- Example 1: Pie Chart -->
          <!-- 4. 프로그램별 참가자 수와 성장률 비교 -->
          <ChartCard title="프로그램별 참가자 수와 성장률 비교" description="이 그래프는 각 프로그램에 등록한 총 참가자 수와 평균 성장률을 시각화합니다."
            chartType="bar" :chartData="programComparisonChartData" :chartOptions="programComparisonChartOptions" />
          <!-- Example 2: Bar Chart -->
          <!-- 5. 주요 성장 지표의 사전/사후 비교 -->
          <ChartCard title="주요 성장 지표의 사전/사후 비교" description="이 그래프는 프로그램 참여 전후의 주요 성장 지표의 변화를 보여줍니다." chartType="bar"
            :chartData="beforeAfterChartData" :chartOptions="beforeAfterChartOptions" />
        </div>
      </main>
    </div>
  </div>
</template>

<!-- <style scoped>
/* Style for the chart container */
.chart-container {
  width: 100%;
  /* Full width */
  max-width: 500px;
  /* Optional: Limit the chart's maximum width */
  margin: 0 auto;
  /* Center the chart horizontally */
}
</style> -->