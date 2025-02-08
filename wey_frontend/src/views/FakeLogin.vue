<template>
  <div class="flex flex-col justify-center font-[sans-serif] sm:h-screen p-4">
    <div class="max-w-md w-full mx-auto border border-gray-300 rounded-2xl p-8">
      <div class="text-center mb-12">
        <!-- <a href="javascript:void(0)"><img src="https://readymadeui.com/readymadeui.svg" alt="logo"
            class='w-40 inline-block' />
        </a> -->
        <div>Reboot Toolbox</div>
      </div>
      <form v-on:submit.prevent="submitForm" class="space-y-6">
        <div class="space-y-6">

          <div>
            <label class="text-white text-sm mb-2 block">이메일</label>
            <input v-model="form.email" type="email" placeholder="Email"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              required />
          </div>
          <div>
            <label class="text-white text-sm mb-2 block">비밀번호</label>
            <input v-model="form.password" type="password" placeholder="Password"
              class="text-white bg-gray-700 border border-gray-600 w-full text-sm px-4 py-3 rounded-md outline-blue-500"
              minlength="8" required />
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
        <p class="text-gray-100 text-sm mt-6 text-center">Forgot <a href="javascript:void(0);"
            class="text-blue-600 font-semibold hover:underline ml-1">Username / Password?</a></p>
        <p class="text-gray-100 text-sm mb-6 text-center">Don't have an account? <a href="javascript:void(0);"
            class="text-blue-600 font-semibold hover:underline ml-1">Sign up</a></p>
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

    return {
      userStore
    }
  },

  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: []
    }
  },
  methods: {
    async submitForm() {
      this.errors = []

      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing')
      }

      if (this.form.password === '') {
        this.errors.push('Your password is missing')
      }

      if (this.errors.length === 0) {
        await axios
          .post('/api/login/', this.form)
          .then(response => {
            this.userStore.setToken(response.data)

            axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
          })
          .catch(error => {
            console.log('error', error)

            this.errors.push('The email or password is incorrect! Or the user is not activated!')
          })
      }

      if (this.errors.length === 0) {
        await axios
          .get('/api/me/')
          .then(response => {
            this.userStore.setUserInfo(response.data)

            this.$router.push('/feed')
          })
          .catch(error => {
            console.log('error', error)
          })
      }
    }
  }
}
</script>