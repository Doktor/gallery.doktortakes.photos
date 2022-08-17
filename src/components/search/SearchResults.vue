<template>
  <section>
    <h2>{{ results.count }} results</h2>

    <PaginationSearch :results="results" @setPage="setPage" />

    <section class="photos">
      <PhotoSearchResult
        v-for="(photo, index) in results.photos"
        :key="index"
        :photo="photo"
      />
    </section>

    <PaginationSearch :results="results" @setPage="setPage" />
  </section>
</template>

<script>
import PaginationSearch from "@/components/search/PaginationSearch";
import PhotoSearchResult from "./PhotoSearchResult.vue";

export default {
  components: {
    PaginationSearch,
    PhotoSearchResult,
  },

  props: {
    results: {
      type: Object,
      required: true,
    },
  },

  methods: {
    setPage(page) {
      this.$emit("setPage", page);
    },
  },
};
</script>

<style scoped>
h2 {
  text-align: left;
}
</style>
