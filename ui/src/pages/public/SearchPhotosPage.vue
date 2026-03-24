<template>
  <section>
    <h2>Search all photos</h2>
    <PhotoSearchForm :results="results" @setResults="setResults" />
    <PhotoSearchResults :results="results" @setPage="setPage" />
  </section>
</template>

<script>
import { useStore } from "@/store";
import PhotoSearchForm from "@/components/search/PhotoSearchForm";
import PhotoSearchResults from "@/components/search/PhotoSearchResults";

export default {
  components: {
    PhotoSearchForm,
    PhotoSearchResults,
  },

  created() {
    useStore().setBreadcrumbs([
      {
        label: "Search",
        to: { name: "search" },
      },
    ]);
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
