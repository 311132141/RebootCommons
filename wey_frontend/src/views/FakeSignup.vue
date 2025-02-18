<template>
  <div class="flex flex-col justify-center font-[sans-serif] sm:h-screen p-4">
    <div class="max-w-md w-full mx-auto border border-gray-300 rounded-2xl p-8">
      <div class="text-center mb-12">
        <!-- <a href="javascript:void(0)"><img src="https://readymadeui.com/readymadeui.svg" alt="logo"
            class='w-40 inline-block' />
        </a> -->
        <div>Reboot Toolbox</div>
        <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
          REBOOT TOOLBOX
        </span>
      </div>
      <form v-on:submit.prevent="submitForm" class="space-y-6">
        <div class="space-y-6">

          <div>
            <label class="text-white text-sm mb-2 block">이름</label>
            <input v-model="form.name" type="text" placeholder="Full Name"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>

          <div>
            <label class="text-white text-sm mb-2 block">이메일</label>
            <input v-model="form.email" type="email" placeholder="Email"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">회사</label>
            <input v-model="form.company" type="company" placeholder="Company"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">비밀번호</label>
            <input v-model="form.password1" type="password" placeholder="Password"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              minlength="8" required />
          </div>

          <div>
            <label class="text-white text-sm mb-2 block">비밀번호 확인</label>
            <input v-model="form.password2" type="password" placeholder="Confirm Password"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>

          <div class="flex items-center">
            <input id="remember-me" name="remember-me" type="checkbox"
              class="h-4 w-4 shrink-0 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
            <label for="remember-me" class="text-gray-100 ml-3 block text-sm">
              I accept the <a href="javascript:void(0);" class="text-blue-600 font-semibold hover:underline ml-1">Terms
                and Conditions</a>
            </label>
          </div>
        </div>


        <template v-if="errors.length > 0">
          <div class="bg-red-300 text-white rounded-lg p-6">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>
        </template>

        <!-- Submit Button -->
        <div class="!mt-8">
          <button type="submit" class="w-full bg-purple-600 text-white p-3 rounded-md hover:bg-purple-700 transition">
            Sign Up
          </button>
        </div>
        <p class="text-gray-100 text-sm mt-6 text-center">Already have an account? <a href="javascript:void(0);"
            class="text-blue-600 font-semibold hover:underline ml-1">Login here</a></p>
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

    return {
      toastStore
    }
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
      errors: [],
    }
  },

  methods: {
    submitForm() {
      this.errors = []

      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing')
      }

      if (this.form.name === '') {
        this.errors.push('Your name is missing')
      }

      if (this.form.company === '') {
        this.errors.push('Your company is missing')
      }

      if (this.form.password1 === '') {
        this.errors.push('Your password is missing')
      }

      if (this.form.password1 !== this.form.password2) {
        this.errors.push('The password does not match')
      }

      if (this.errors.length === 0) {
        axios
          .post('/api/signup/', this.form)
          .then(response => {
            if (response.data.message === 'success') {
              this.toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link.', 'bg-emerald-500')

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

              this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
            }
          })
          .catch(error => {
            console.log('error', error)
          })
      }
    }
  }
}
</script>