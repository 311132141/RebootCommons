<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- Sidebar -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

                <p><strong>Survey Application</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">Surveys Completed: {{ surveys.length }}</p>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-center col-span-2 space-y-4">
            <!-- Survey Form -->
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitSurvey" method="post" class="space-y-4 p-4">
                    <div>
                        <label for="gender" class="block text-sm font-medium text-gray-700">Gender</label>
                        <select v-model="surveyData.gender" id="gender"
                            class="mt-1 block w-full rounded-lg bg-gray-100">
                            <option disabled value="">Select Gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                        </select>
                    </div>

                    <div>
                        <label for="age" class="block text-sm font-medium text-gray-700">Age Group</label>
                        <select v-model="surveyData.age" id="age" class="mt-1 block w-full rounded-lg bg-gray-100">
                            <option disabled value="">Select Age Group</option>
                            <option value="20">20s</option>
                            <option value="30">30s</option>
                            <option value="40">40s</option>
                            <option value="50">50s</option>
                            <option value="60">60s</option>
                        </select>
                    </div>

                    <div>
                        <label for="marital_status" class="block text-sm font-medium text-gray-700">Marital
                            Status</label>
                        <select v-model="surveyData.marital_status" id="marital_status"
                            class="mt-1 block w-full rounded-lg bg-gray-100">
                            <option disabled value="">Select Marital Status</option>
                            <option value="single">Single</option>
                            <option value="married">Married</option>
                        </select>
                    </div>

                    <div>
                        <label for="education" class="block text-sm font-medium text-gray-700">Education</label>
                        <select v-model="surveyData.education" id="education"
                            class="mt-1 block w-full rounded-lg bg-gray-100">
                            <option disabled value="">Select Education Level</option>
                            <option value="highschool">High School</option>
                            <option value="diploma">Diploma</option>
                            <option value="bachelor">Bachelor</option>
                            <option value="master">Master</option>
                            <option value="phd">PhD</option>
                        </select>
                    </div>

                    <button type="submit"
                        class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg w-full">Submit Survey</button>
                </form>
            </div>

            <!-- Survey List -->
            <div v-for="survey in surveys" v-bind:key="survey.id"
                class="p-4 bg-white border border-gray-200 rounded-lg">
                <div class="mb-6 flex items-center justify-between">
                    <div class="flex items-center space-x-6">
                        <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                        <p><strong>{{ survey.user_name || 'Anonymous' }}</strong></p>
                    </div>
                    <p class="text-gray-600">{{ survey.created_at_formatted || 'Just now' }}</p>
                </div>
                <p>Gender: {{ survey.gender }}</p>
                <p>Age Group: {{ survey.age }}</p>
                <p>Marital Status: {{ survey.marital_status }}</p>
                <p>Education: {{ survey.education }}</p>
            </div>
        </div>

        <!-- Right Sidebar -->
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'

export default {
    name: 'SurveyView',

    components: {
        PeopleYouMayKnow,
        Trends,
    },

    data() {
        return {
            surveys: [],
            surveyData: {
                gender: '',
                age: '',
                marital_status: '',
                education: '',
            },
        }
    },

    mounted() {
        this.getSurveys()
    },

    methods: {
        getSurveys() {
            axios
                .get('/api/survey/')
                .then(response => {
                    console.log('Surveys fetched:', response.data)
                    this.surveys = response.data
                })
                .catch(error => {
                    console.error('Error fetching surveys:', error)
                })
        },

        submitSurvey() {
            axios
                .post('/api/survey/create/', {
                    gender: this.surveyData.gender,
                    age: this.surveyData.age,
                    marital_status: this.surveyData.marital_status,
                    education: this.surveyData.education,
                })
                .catch(error => {
                    console.error('Error submitting survey:', error)
                })
        },

        resetSurveyForm() {
            this.surveyData = {
                gender: '',
                age: '',
                marital_status: '',
                education: '',
            }
        },
    },
}
</script>
