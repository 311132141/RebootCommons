import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

import VueApexCharts from 'vue3-apexcharts';
import 'chart.js'; // Import Chart.js
import PrimeVue from 'primevue/config';
import { definePreset } from '@primevue/themes';
import Aura from '@primevue/themes/aura';


import './assets/main.css'

// axios.defaults.baseURL = import.meta.env.VITE_API_URL
axios.defaults.baseURL = 'http://127.0.0.1:8000'
document.documentElement.classList.add('dark'); // Default to dark mode

const app = createApp(App)


const MyPreset = definePreset(Aura, {
  semantic: {
      colorScheme: {
          light: {
              surface: {
                  0: '#ffffff',
                  50: '{zinc.50}',
                  100: '{zinc.100}',
                  200: '{zinc.200}',
                  300: '{zinc.300}',
                  400: '{zinc.400}',
                  500: '{zinc.500}',
                  600: '{zinc.600}',
                  700: '{zinc.700}',
                  800: '{zinc.800}',
                  900: '{zinc.900}',
                  950: '{zinc.950}'
              }
          },
          dark: {
              surface: {
                  0: '#ffffff',
                  50: '{slate.50}',
                  100: '{slate.100}',
                  200: '{slate.200}',
                  300: '{slate.300}',
                  400: '{slate.400}',
                  500: '{slate.500}',
                  600: '{slate.600}',
                  700: '{slate.700}',
                  800: '{slate.800}',
                  900: '{slate.900}',
                  950: '{slate.950}'
              }
          }
      }
  }
});
document.documentElement.classList.add('my-app-dark');

app.use(PrimeVue, {
  theme: {
      preset: MyPreset,
      options: {
        darkModeSelector: ".my-app-dark",
      },
  },
});


app.use(VueApexCharts);
app.component('ApexChart', VueApexCharts);
app.use(createPinia())
app.use(router, axios)

app.mount('#app')
