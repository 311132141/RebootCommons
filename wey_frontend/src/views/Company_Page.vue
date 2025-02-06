<template>
  <div class="bg-[#1a1b1e] min-h-screen text-white">
    <div class="p-4">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-2 text-gray-400">
          <span>Dashboard</span>
          <span>></span>
          <span>Companies</span>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input type="text" placeholder="Search"
              class="bg-[#25262b] rounded-md px-4 py-2 pl-10 text-sm w-64 focus:outline-none" />
            <svg class="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none"
              stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <button class="bg-[#25262b] p-2 rounded-md">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
          </button>
        </div>
      </div>

      <h1 class="text-2xl font-medium mb-6">기업 관리 대시보드</h1>

      <!-- Companies List -->
      <div class="bg-[#1d1e22] rounded-lg overflow-hidden">
        <div class="p-4 border-b border-gray-800">
          <h2 class="text-lg">전체 기업 현황 및 성과 데이터</h2>
        </div>

        <!-- Table Header -->
        <div class="grid grid-cols-6 gap-4 px-4 py-3 text-sm text-gray-400">
          <div>이름</div>
          <div>담당자 정보</div>
          <div>참여 프로그램</div>
          <div>협업 성장률</div>
          <div>리포트 생성</div>
          <div>대시보드 열기</div>
        </div>

        <!-- Company Rows -->
        <div class="space-y-px">
          <div v-for="company in companies" :key="company.email"
            class="grid grid-cols-6 gap-4 px-4 py-3 bg-[#25262b] hover:bg-[#2c2d31] transition-colors items-center">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-full bg-gray-600 flex items-center justify-center">
                <span class="text-sm">{{ getInitials(company.name) }}</span>
              </div>
              <div>
                <div class="font-medium">{{ company.name }}</div>
                <div class="text-sm text-gray-400">{{ company.email }}</div>
              </div>
            </div>
            <div>{{ company.phone }}</div>
            <div>{{ company.programs }}</div>
            <div>{{ company.growth }}</div>
            <div>
              <button
                class="px-3 py-1.5 bg-[#1d1e22] rounded-md text-sm hover:bg-[#2c2d31] transition-colors flex items-center space-x-1">
                <span class="material-icons-outlined text-sm">description</span>
                <span>리포트 작성하기</span>
              </button>
            </div>
            <div>
              <button
                class="px-3 py-1.5 bg-[#1d1e22] rounded-md text-sm hover:bg-[#2c2d31] transition-colors flex items-center space-x-1">
                <span class="material-icons-outlined text-sm">dashboard</span>
                <span>대시보드 열기</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      companies: [
        {
          name: 'Company A',
          email: 'CompanyA@gmail.com',
          phone: '(010)000-0000',
          programs: '비전, 리더십, 기업',
          growth: '20%'
        },
        {
          name: 'Company A',
          email: 'CompanyA@gmail.com',
          phone: '(010)000-0000',
          programs: '비전, 리더십, 기업',
          growth: '20%'
        },
        {
          name: 'Company A',
          email: 'CompanyA@gmail.com',
          phone: '(010)000-0000',
          programs: '비전, 리더십, 기업',
          growth: '20%'
        },
        // Add more companies as needed
      ]
    }
  },
  methods: {
    getInitials(name) {
      return name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
    }
  }
}
</script>