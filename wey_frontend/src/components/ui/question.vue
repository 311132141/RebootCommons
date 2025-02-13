<template>
  <div class="mb-6">
    <!-- 질문 제목 -->
    <!-- <label class="block font-bold text-lg mb-4">{{ question.text }}</label> -->

    <!-- Text Input -->
    <!-- <template v-if="question.type === 'text'">
      <input type="text" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"
        class="w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
    </template> -->

    <!-- Single Choice -->
    <template v-if="question.type === radio">
      <div class="relative flex flex-col min-h-[calc(100vh_-_16vh)] md:hidden">
        <!-- Scrollable Content -->
        <div class="flex-1 overflow-auto  pt-6">
          <p class="text-white">
            {{ question.text }}
          </p>
        </div>

        <!-- Sticky Options & Button Container -->
        <div class="sticky bottom-0 left-0 right-0 bg-gray-900 shadow-lg  py-5">
          <div class="w-full flex flex-col items-center gap-2">
            <!-- Question Options -->
            <button v-for="option in question.options" :key="option.id || option"
              @click="$emit('update:modelValue', option.id || option)" :class="[
                'w-full py-[1.1rem] rounded-2xl transition-colors',
                modelValue === (option.id || option)
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              ]">
              <b2>{{ option.name || option }}</b2>
            </button>

            <!-- Next Button -->
            <button @click="$emit('next-question')"
              class="mt-4 w-full py-[1.1rem] rounded-2xl transition-colors bg-purple-700 text-gray-300 hover:bg-purple-600">
              <b2>다음</b2>
            </button>
          </div>
        </div>
      </div>
      <div class=" hidden md:flex items-center justify-center min-h-[calc(100vh_-_13vh)] ">
        <div data-layer="Frame 660"
          class=" w-[30rem] lg:w-[36rem] flex-col justify-start items-center gap-14 inline-flex">
          <div data-layer="Group 26" class="flex-col items-center justify-center gap-4 inline-flex">
            <b2>{{ question.category }}</b2>
            <h4 class="font-bold">{{ question.text }}</h4>

          </div>
          <div class=" w-full flex justify-center pb-9 flex-col items-center gap-2 mb-24 ">
            <button v-for="option in question.options" :key="option.id || option"
              @click="$emit('update:modelValue', option.id || option)" :class="[
                'w-full py-[1.25rem] rounded-2xl transition-colors',
                modelValue === (option.id || option)
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              ]">
              <b2>{{ option.name || option }}</b2>
            </button>

          </div>
          <!-- <div class=" w-full flex justify-center pb-9 flex-col items-center gap-2 ">
            <button @click="$emit('next-question')"
              class="mt-8 w-full py-5 rounded-2xl transition-colors bg-purple-700 text-gray-300 hover:bg-purple-600">
              <b2>
                다음
              </b2>
            </button>
          </div> -->
        </div>
      </div>
      <div class="w-full py-4  text-center  fixed bottom-10 left-0 right-0">
        <div class="w-[30rem] lg:w-[36rem] flex-col justify-start items-center gap-14  hidden md:inline-flex">
          <div class=" w-full flex justify-center pb-9 flex-col items-center gap-2 ">
            <button v-if="!isLastPage" @click="$emit('next-question')"
              class="mt-8 w-full py-5 rounded-2xl transition-colors bg-purple-700 text-gray-300 hover:bg-purple-600">
              <b2>
                다음
              </b2>
            </button>
            <button v-else @click="$emit('submit-survey')"
              class="mt-8 w-full py-5 rounded-2xl transition-colors bg-purple-700 text-gray-300 hover:bg-purple-600">
              <b2>
                제출하기
              </b2>
            </button>
          </div>
        </div>
      </div>

    </template>

    <!-- Multiple Choice -->
    <template v-else-if="question.type === checkbox">
      <div class="space-y-3">
        <button v-for="option in question.options" :key="option" @click="toggleOption(option)" :class="[
          'w-full text-left px-4 py-3 rounded-lg font-medium transition-colors',
          modelValue.includes(option)
            ? 'bg-blue-500 text-white'
            : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
        ]">
          {{ option }}
        </button>
      </div>
    </template>
    <!-- Likert Scale -->
    <template v-else-if="question.type === rating">
      <div class="w-full max-w-2xl mx-auto p-6">
        <div class="mb-6 text-center text-white text-lg">
          {{ question.text }}
        </div>

        <div class="flex flex-col space-y-2">
          <div class="flex justify-between items-center">
            <div class="grid grid-cols-5 gap-4 w-full mx-8">
              <template v-for="n in (question.points || 5)" :key="n">
                <div class="flex flex-col items-center">
                  <button @click="$emit('update:modelValue', n)"
                    class="w-12 h-12 rounded-full border-2 transition-all duration-200 focus:outline-none" :class="[
                      modelValue === n
                        ? 'border-blue-500 bg-blue-500'
                        : 'border-gray-400 bg-transparent hover:border-blue-300'
                    ]">
                    <span class="sr-only">Option {{ n }}</span>
                  </button>
                </div>
              </template>
            </div>
          </div>

          <div class="flex justify-between text-gray-400 px-4">
            <span>{{ question.labels?.left || '전혀 그렇지 않다' }}</span>
            <span>{{ question.labels?.right || '매우 그렇다' }}</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    question: Object,
    modelValue: {
      type: [String, Array],
      default: null,
    },
  },
  emits: ["update:modelValue", "next-question", "submit-survey"], // Declare the emitted event
  methods: {
    toggleOption(option) {
      // 다중 선택 값 업데이트
      const newValue = [...(this.modelValue || [])];
      const index = newValue.indexOf(option);
      if (index === -1) {
        newValue.push(option); // 선택 추가
      } else {
        newValue.splice(index, 1); // 선택 제거
      }
      this.$emit("update:modelValue", newValue);
    },
  },
};
</script>