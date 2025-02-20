<template>
  <div class="flex h-screen">
    <main class="flex-1 p-6 ">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-2 text-gray-400">
          <span>Dashboard</span>
          <span>></span>

          <span>Users</span>
        </div>
      </div>
      <h1 class="text-2xl font-medium mb-6">개인 대시보드</h1>

      <div class="flex items-center justify-center bg-gray-900 text-white ">
        <div class="w-full h-full">
          <table class="w-full bg-gray-800 rounded-lg overflow-hidden shadow-lg">
            <thead class="hidden sm:table-header-group bg-gray-900">
              <tr class="text-xs sm:text-sm text-gray-400">
                <th class="p-3 text-left">이름</th>
                <th class="p-3 text-left">참여 프로그램</th>
                <th class="p-3 text-left">성장률</th>
                <th class="p-3 text-left" width="130px">대시보드 열기</th>
                <th class="p-3 text-left" width="130px">삭제</th> <!-- New Delete Column -->
              </tr>
            </thead>
            <tbody class="block sm:table-row-group">
              <tr v-for="user in users" :key="user.id" class="block sm:table-row border-b border border-gray-900 ">
                <!-- Name Column -->
                <td class="block sm:table-cell p-3" data-label="이름">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-full bg-gray-600 flex items-center justify-center">
                      <span class="text-xs sm:text-sm">{{ getInitials(user.name) }}</span>
                    </div>
                    <div>
                      <div class="font-medium text-blue-400 hover:underline cursor-pointer"
                        @click.stop="goToCompanyDetails(user.id)">
                        {{ user.name }}
                      </div>
                      <div class="text-xs sm:text-sm text-gray-400">{{ user.email }}</div>
                    </div>
                  </div>
                </td>

                <!-- 참여 프로그램 -->
                <td class="block sm:table-cell p-3" data-label="참여 프로그램">
                  {{ user.programs }}
                </td>

                <!-- 협업 성장률 -->
                <td class="block sm:table-cell p-3" data-label="협업 성장률">
                  {{ user.growth }}
                </td>

                <!-- Dashboard Button -->
                <td class="block sm:table-cell p-3" data-label="대시보드 열기">
                  <button @click="openDashboard(user)"
                    class="px-3 py-1.5 bg-gray-900 rounded-md text-xs sm:text-sm hover:bg-gray-600 transition-colors">
                    대시보드 열기
                  </button>
                </td>

                <!-- Delete Button -->
                <td class="block sm:table-cell p-3" data-label="삭제">
                  <button @click="deleteUser(user.id)"
                    class="px-3 py-1.5 bg-red-600 rounded-md text-xs sm:text-sm hover:bg-red-700 transition-colors">
                    삭제
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
import axios from "axios";

export default {
  props: ["id"],
  data() {
    return {
      companyName: "",
      users: [],
    };
  },
  mounted() {
    this.fetchCompanyUsers();
    console.log("DEBUG: UserNoCompany page loaded");
  },
  methods: {
    async fetchCompanyUsers() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/users/no-company/");
        this.users = response.data;
      } catch (error) {
        console.error("Failed to fetch users without company:", error);
      }
    },
    getInitials(name) {
      return name
        .split(" ")
        .map((word) => word[0])
        .join("")
        .toUpperCase();
    },
    openDashboard(user) {
      this.$router.push({ name: "ProfileView", params: { id: user.id } });
    },
    goToCompanyDetails(userId) {
      // Assuming this method exists; adjust as needed
      this.$router.push({ name: "UserDetails", params: { id: userId } });
    },
    async deleteUser(userId) {
      if (!confirm("정말로 이 사용자를 삭제하시겠습니까?")) return; // Confirmation prompt

      try {
        // Get the token from localStorage (or your auth system)
        const token = localStorage.getItem("access_token"); // Adjust based on your auth setup
        if (!token) {
          alert("로그인이 필요합니다.");
          return;
        }

        // Make DELETE request to backend
        const response = await axios.delete(
          `http://127.0.0.1:8000/api/users/${userId}/delete`,
          {
            headers: {
              Authorization: `Bearer ${token}`, // JWT token for authentication
            },
          }
        );

        // On success, remove user from the list
        this.users = this.users.filter((user) => user.id !== userId);
        alert(response.data.message); // Show success message from backend
      } catch (error) {
        console.error("Failed to delete user:", error);
        if (error.response) {
          alert(error.response.data.error || "사용자 삭제에 실패했습니다.");
        } else {
          alert("서버와의 연결에 문제가 있습니다.");
        }
      }
    },
  },
};
</script>