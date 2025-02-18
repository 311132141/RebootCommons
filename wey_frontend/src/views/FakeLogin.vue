<template>
  <div class="flex flex-col justify-center font-[sans-serif] sm:h-screen p-4">
    <div class="max-w-md w-full mx-auto border border-gray-300 rounded-2xl p-8">
      <div class="text-center mb-12">
        <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
          REBOOT TOOLBOX
        </span>
      </div>
      <form v-on:submit.prevent="submitForm" class="space-y-6">
        <div class="space-y-6">
          <div>
            <label class="text-white text-sm mb-2 block">이메일</label>
            <input v-model="form.email" type="email" placeholder="이메일 주소를 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">비밀번호</label>
            <input v-model="form.password" type="password" placeholder="비밀번호를 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              minlength="8" required />
          </div>
          <div class="flex items-center">
            <input id="remember-me" name="remember-me" type="checkbox"
              class="h-4 w-4 shrink-0 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
            <label for="remember-me" class="text-gray-100 ml-3 block text-sm">
              이용 약관에 동의합니다.
            </label>
          </div>
        </div>

        <template v-if="errors.length > 0">
          <div class="bg-red-300 text-white rounded-lg p-6">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </div>
        </template>

        <div class="!mt-8">
          <button type="submit" class="w-full bg-purple-600 text-white p-3 rounded-md hover:bg-purple-700 transition">
            로그인
          </button>
        </div>

        <router-link to="/fakesignup">
          <p class="text-gray-100 text-sm mt-6 mb-6 text-center">
            계정이 없으신가요?
            <span class="text-blue-500 font-semibold hover:underline ml-1">회원가입</span>
          </p>
        </router-link>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      errors: []
    }
  },
  methods: {
    async submitForm() {
      this.errors = []
      console.log("폼 제출됨:", this.form)

      if (this.form.email === "") {
        this.errors.push("이메일을 입력해주세요.")
      }
      if (this.form.password === "") {
        this.errors.push("비밀번호를 입력해주세요.")
      }
      if (this.errors.length > 0) return

      try {
        console.log("로그인 요청 중...")
        const response = await axios.post("/api/login/", this.form)
        console.log("로그인 성공, 토큰 수신:", response.data)

        this.userStore.setToken(response.data)
        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
        console.log("인증 헤더 설정됨:", axios.defaults.headers.common["Authorization"])

        localStorage.setItem("access_token", response.data.access)
        localStorage.setItem("refresh_token", response.data.refresh)
      } catch (error) {
        console.error("로그인 실패:", error)
        this.errors.push("이메일 또는 비밀번호가 올바르지 않거나, 계정이 활성화되지 않았습니다.")
        return
      }

      try {
        console.log("사용자 정보 조회 중...")
        const userResponse = await axios.get("/api/me/")
        console.log("사용자 정보 수신:", userResponse.data)

        this.userStore.setUserInfo(userResponse.data)
        localStorage.setItem("user_info", JSON.stringify(userResponse.data))
        console.log("페이지 이동 중: /figma")
        this.$router.push("/figma")
      } catch (error) {
        console.error("사용자 정보 조회 실패:", error)
        this.errors.push("사용자 정보를 가져오지 못했습니다.")
      }
    }
  }
}
</script>