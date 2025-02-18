<template>
  <div class="flex flex-col justify-center font-[sans-serif] sm:h-screen p-4">
    <div class="max-w-md w-full mx-auto border border-gray-300 rounded-2xl p-8">
      <div class="text-center mb-12">
        <div>회사 등록</div>
      </div>
      <form v-on:submit.prevent="submitForm" class="space-y-6">
        <div class="space-y-6">
          <div>
            <label class="text-white text-sm mb-2 block">회사 이름</label>
            <input v-model="form.name" type="text" placeholder="회사 이름을 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">코스 선택</label>
            <select v-model="form.course" required
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500">
              <option disabled value="">코스를 선택하세요</option>
              <option value="비전하우스">비전하우스</option>
              <option value="리더십과 혁신">리더십과 혁신</option>
              <option value="기업가정신과 혁신">기업가정신과 혁신</option>
            </select>
          </div>
        </div>

        <template v-if="errors.length > 0">
          <div class="bg-red-400 text-white rounded-lg p-6">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </div>
        </template>

        <div class="!mt-8">
          <button type="submit" class="w-full bg-purple-600 text-white p-3 rounded-md hover:bg-purple-700 transition">
            등록
          </button>
        </div>
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
        name: '',
        course: '',
      },
      errors: []
    }
  },
  methods: {
    async submitForm() {
      this.errors = []
      console.log("폼 제출됨:", this.form)

      if (!this.form.name) {
        this.errors.push("회사 이름을 입력해주세요.")
      }

      if (!this.form.course) {
        this.errors.push("코스를 선택해주세요.")
      }

      if (this.errors.length > 0) {
        return
      }

      try {
        console.log("회사 등록 요청 중...")
        const response = await axios.post("/api/company/register/", this.form)
        console.log("등록 성공, 응답 수신:", response.data)
        // Pop up a success prompt after registration
        alert("등록에 성공했습니다!")
      } catch (error) {
        console.error("회사 등록 실패:", error)
        this.errors.push("회사 등록에 실패했습니다. 입력하신 정보를 확인해주세요.")
        return
      }

    }
  }
}
</script>

