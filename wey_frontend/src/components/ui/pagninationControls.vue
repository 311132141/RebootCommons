<template>
  <div class="flex justify-between mt-6">
    <button type="button" :disabled="currentPage === 1" @click="$emit('prev')"
      class="bg-gray-300 px-4 py-2 rounded disabled:opacity-50">
      Previous
    </button>
    <button type="button" :disabled="currentPage === totalPages" @click="$emit('next')"
      class="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50">
      Next
    </button>
  </div>
</template>

<script>
export default {
  props: {
    currentPage: Number,
    totalPages: Number,
  },
};
</script>