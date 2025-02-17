<template>
  <div class="flex h-screen">
    <main class="flex-1 p-6 ">

      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-2 text-gray-400">
          <span>Dashboard</span>
          <span>></span>
          <span>Companies</span>
        </div>
        <!-- <div class="flex items-center space-x-4">
          <div class="relative">
            <input type="text" placeholder="Search"
              class="bg-gray-900 rounded-md px-4 py-2 pl-10 text-sm w-64 focus:outline-none" />
            <svg class="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none"
              stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <button class="bg-gray-900 p-2 rounded-md">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
          </button>
        </div> -->
      </div>
      <h1 class="text-2xl font-medium mb-6">기업 관리 대시보드</h1>

      <div class="flex items-center justify-center bg-gray-900 text-white ">
        <div class="w-full h-full">
          <table class="w-full bg-gray-800 rounded-lg overflow-hidden shadow-lg">
            <thead class="hidden sm:table-header-group bg-gray-900">

              <tr class="text-xs sm:text-sm text-gray-400">
                <th class="p-3 text-left">이름</th>

                <th class="p-3 text-left">참여 프로그램</th>
                <th class="p-3 text-left">협업 성장률</th>
                <th class="p-3 text-left" width="130px">대시보드 열기</th>
              </tr>
            </thead>
            <tbody class="block sm:table-row-group">
              <tr v-for="company in companies" :key="company.id"
                class="block sm:table-row border-b border border-gray-900 ">

                <!-- Name Column -->
                <td class="block sm:table-cell p-3 " data-label="이름">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-full bg-gray-600 flex items-center justify-center">
                      <span class="text-xs sm:text-sm">{{ getInitials(company.name) }}</span>
                    </div>
                    <div>
                      <div class="font-medium text-blue-400 hover:underline cursor-pointer"
                        @click.stop="goToCompanyDetails(company.id)">
                        {{ company.name }}
                      </div>
                      <div class="text-xs sm:text-sm text-gray-400">{{ company.email }}</div>
                    </div>
                  </div>
                </td>



                <!-- 참여 프로그램 -->
                <td class="block sm:table-cell p-3" data-label="참여 프로그램">
                  {{ company.programs }}
                </td>

                <!-- 협업 성장률 -->
                <td class="block sm:table-cell p-3" data-label="협업 성장률">
                  {{ company.growth }}
                </td>

                <!-- Dashboard Button -->
                <td class="block sm:table-cell p-3" data-label="대시보드 열기">
                  <button @click="goToCompanyDashboard(company.id)"
                    class="px-3 py-1.5 bg-gray-900 rounded-md text-xs sm:text-sm hover:bg-gray-600 transition-colors">
                    대시보드 열기
                  </button>
                </td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>




    </main>
  </div>
</template>
<style scoped>
@media (max-width: 639px) {
  thead {
    display: none;
  }

  tbody {
    display: flex;
    flex-direction: column;
  }

  tr {
    display: flex;
    flex-direction: column;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 10px;
    margin-bottom: 10px;
  }

  td {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    border-bottom: none;
    font-size: 14px;
  }

  td::before {
    content: attr(data-label);
    font-weight: bold;
    color: rgba(255, 255, 255, 0.7);
  }
}
</style>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      companies: [],
    };
  },
  mounted() {
    this.fetchCompanies();
  },
  methods: {
    async fetchCompanies() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/companies/');
        this.companies = response.data.companies;
      } catch (error) {
        console.error("Failed to fetch companies:", error);
      }
    },
    goToCompanyDetails(companyId) {
      console.log(`Navigating to company: ${companyId}`);
      this.$router.push({ name: 'company-details', params: { id: companyId } });
    },
    goToCompanyDashboard(companyId) {
      console.log(`Navigating to company dashboard: ${companyId}`);
      this.$router.push({ name: "company-dashboard", params: { id: companyId } });
    },
    getInitials(name) {
      return name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase();
    }
  }
};
</script>
