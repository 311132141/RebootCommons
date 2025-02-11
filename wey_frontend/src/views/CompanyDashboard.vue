<template>

  <div class="flex h-screen" v-if="!loading">


    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Navbar -->
      <main class="flex-1 p-6 ">
        <div class="text-3xl text-bold pb-3 print:text-black ">Overview</div>
        <button @click="printDashboard"
          class=" bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 print:hidden">
          Print
        </button>
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
            <div class="col-span-12 sm:col-span-5 md:col-span-5  lg:col-span-5 ">
              <ChartCard title="Leadership Comparison"
                description="Comparison between Male and Female leadership ratings"
                :labels="['남성 (Male)', '여성 (Female)']" title_z="Leadership Category" title_y="Average Score"
                :chartType="'pie'" />

            </div>
            <div class="col-span-12 sm:col-span-7 md:col-span-7 lg:col-span-7">

              <ChartCard canvasId="leadershipChart" title="Leadership Comparison"
                description="Comparison between Male and Female leadership ratings" :labels="leadershipLabels"
                :datasets="computedDatasets" title_z="Leadership Category" title_y="Average Score" :chartType="'bar'" />


            </div>
          </div>
          <div class="grid grid-cols-12 gap-5 ">
            <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-6 ">
              <ChartCard_radar title="Leadership & Lifestyle Growth"
                description="Comparison of improvements in Leadership Programs and Lifestyle"
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

              <ChartCard canvasId="demographicChart-age" title="age bro" description="i cbb living"
                :labels="demographicLabels.salary" :datasets="demographicDatasets.age" title_z="end this life"
                title_y="end" :chartType="'bar'" />


            </div>
          </div>
          <div class="grid grid-cols-12 gap-5 pb-5">
            <div class="col-span-12 sm:col-span-12 lg:col-span-12 ">
              <HeatmapChart title="Lifestyle & Course Growth"
                description="Shows how lifestyle factors impact course improvements"
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
            <div class="col-span-12 sm:col-span-6 md:col-span-6  lg:col-span-6 ">
              <ChartCard canvasId="demographicChart-age" title="age bro" description="i cbb living"
                :labels="demographicLabels.salary" :datasets="demographicDatasets.salary" title_z="end this life"
                title_y="end" :chartType="'bar'" />

            </div>
            <div class="col-span-12 sm:col-span-6 md:col-span-6 lg:col-span-6">

              <ChartCard canvasId="demographicChart-age" title="age bro" description="i cbb living"
                :labels="demographicLabels.marital" :datasets="demographicDatasets.marital" title_z="end this life"
                title_y="end" :chartType="'bar'" />


            </div>
          </div>
          <div class="grid grid-cols-12 gap-5 ">
            <div class="col-span-12 sm:col-span-12 md:col-span-12  lg:col-span-12 ">
              <ChartCard canvasId="demographicChart-age" title="age bro" description="i cbb living"
                :labels="demographicLabels.education" :datasets="demographicDatasets.education" title_z="end this life"
                title_y="end" :chartType="'bar'" />

            </div>

          </div>
          <!-- Row 2: Age Distribution and Age Improvement Comparison -->


          <!-- Row 3: Job Distribution and Job Salary Comparison -->


        </div>
      </main>
    </div>
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