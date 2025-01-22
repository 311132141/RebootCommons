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
            <!-- Survey Type Selection -->
            <div v-if="!surveyType" class="bg-white border border-gray-200 rounded-lg p-4 text-center">
                <p class="mb-4">Choose a Survey Type</p>
                <button 
                    @click="setSurveyType('기업용')" 
                    class="inline-block py-4 px-6 bg-blue-600 text-white rounded-lg mr-4">
                    Corporate
                </button>
                <button 
                    @click="setSurveyType('개인용')" 
                    class="inline-block py-4 px-6 bg-green-600 text-white rounded-lg">
                    Individual
                </button>
            </div>

            <!-- Survey Form -->
            <div v-else class="bg-white border border-gray-200 rounded-lg">
                <form @submit.prevent="submitSurvey" class="space-y-4 p-4">
                    <div v-for="question in surveyQuestions" :key="question.id" class="space-y-2">
                        <label :for="question.id" class="block text-sm font-medium text-gray-700">{{ question.text }}</label>
                        <select 
                            v-model="surveyData[question.id]" 
                            :id="question.id" 
                            class="mt-1 block w-full rounded-lg bg-gray-100">
                            <option disabled value="">Select an option</option>
                            <option v-for="option in question.options" :key="option" :value="option">
                                {{ option }}
                            </option>
                        </select>
                    </div>
                    <button type="submit" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg w-full">
                        Submit Survey
                    </button>
                </form>
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
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";

export default {
    name: "SurveyView",

    components: { PeopleYouMayKnow, Trends },

    data() {
        return {
            surveys: [],
            surveyType: "",
            surveyQuestions: [],
            surveyData: {},
        };
    },

    methods: {
        setSurveyType(type) {
            this.surveyType = type;
            this.fetchSurveyQuestions();
        },

        fetchSurveyQuestions() {
            axios
                .get(`/api/survey/${this.surveyType}/`)
                .then((response) => {
                    this.surveyQuestions = response.data.questions;
                    this.initializeSurveyData();
                })
                .catch((error) => {
                    console.error("Error fetching survey questions:", error);
                });
        },

        initializeSurveyData() {
            this.surveyData = {};
            this.surveyQuestions.forEach((question) => {
                this.surveyData[question.id] = "";
            });
        },

        submitSurvey() {
            axios
                .post(`/api/survey/${this.surveyType}/`, { answers: this.surveyData })
                .then((response) => {
                    console.log("Survey submitted:", response.data);
                    this.surveys.push(response.data);
                })
                .catch((error) => {
                    console.error("Error submitting survey:", error);
                });
        },
    },
};
</script>
