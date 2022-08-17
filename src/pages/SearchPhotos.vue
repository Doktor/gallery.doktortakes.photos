<template>
  <section>
    <h2>Search all photos</h2>
    <SearchPhotoForm :results="results" @setResults="setResults" />
    <SearchResults :results="results" @setPage="setPage" />
  </section>
</template>

<script>
import SearchPhotoForm from "@/components/search/SearchPhotoForm.vue";
import SearchResults from "@/components/search/SearchResults";

export default {
  components: {
    SearchPhotoForm,
    SearchResults,
  },

  data() {
    return {
      results: {
        page: 1,
        itemsPerPage: 24,
        photos: [],
        count: 0,
      },
    };
  },

  methods: {
    setPage(page) {
      this.results.page = page;
    },
    setResults(results) {
      this.results = results;
    },
  },
};
</script>
