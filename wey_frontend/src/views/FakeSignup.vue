<template>
  <div class="flex flex-col justify-center font-[sans-serif] sm:h-screen p-4">
    <div class="max-w-md w-full mx-auto border border-gray-300 rounded-2xl p-8">
      <div class="text-center mb-12">
        <div>리부트 툴박스</div>
        <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
          REBOOT TOOLBOX
        </span>
      </div>
      <form v-on:submit.prevent="submitForm" class="space-y-6">
        <div class="space-y-6">
          <div>
            <label class="text-white text-sm mb-2 block">이름</label>
            <input v-model="form.name" type="text" placeholder="이름을 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">이메일</label>
            <input v-model="form.email" type="email" placeholder="이메일 주소를 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">회사</label>
            <input v-model="form.company" type="text" placeholder="회사명을 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">비밀번호</label>
            <input v-model="form.password1" type="password" placeholder="비밀번호를 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              minlength="8" required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">비밀번호 확인</label>
            <input v-model="form.password2" type="password" placeholder="비밀번호를 다시 입력하세요"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
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
            회원가입
          </button>
        </div>

        <router-link to="/fakelogin">
          <p class="text-gray-100 text-sm mt-6 mb-6 text-center">
            이미 계정이 있으신가요?
            <span class="text-blue-500 font-semibold hover:underline ml-1">로그인하기</span>
          </p>
        </router-link>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'

export default {
  setup() {
    const toastStore = useToastStore()
    return { toastStore }
  },
  data() {
    return {
      form: {
        email: '',
        name: '',
        company: '',
        password1: '',
        password2: ''
      },
      errors: []
    }
  },
  methods: {
    submitForm() {
      this.errors = []
      if (this.form.email === '') {
        this.errors.push('이메일을 입력해주세요.')
      }
      if (this.form.name === '') {
        this.errors.push('이름을 입력해주세요.')
      }
      if (this.form.company === '') {
        this.errors.push('회사명을 입력해주세요.')
      }
      if (this.form.password1 === '') {
        this.errors.push('비밀번호를 입력해주세요.')
      }
      if (this.form.password1 !== this.form.password2) {
        this.errors.push('비밀번호가 일치하지 않습니다.')
      }
      if (this.errors.length === 0) {
        axios
          .post('/api/signup/', this.form)
          .then(response => {
            if (response.data.message === 'success') {
              this.toastStore.showToast(
                5000,
                '회원가입이 완료되었습니다. 이메일에 전송된 링크를 클릭하여 계정을 활성화해주세요.',
                'bg-emerald-500'
              )
              this.form.email = ''
              this.form.name = ''
              this.form.company = ''
              this.form.password1 = ''
              this.form.password2 = ''
            } else {
              const data = JSON.parse(response.data.message)
              for (const key in data) {
                this.errors.push(data[key][0].message)
              }
              this.toastStore.showToast(5000, '문제가 발생했습니다. 다시 시도해주세요.', 'bg-red-300')
            }
          })
          .catch(error => {
            console.error('회원가입 실패:', error)
            this.toastStore.showToast(5000, '서버 오류가 발생했습니다. 다시 시도해주세요.', 'bg-red-300')
          })
      }
    }
  }
}
</script>