<template>
  <section>
    <h2>{{ results.count }} results</h2>

    <Pagination
      :itemsPerPage="results.itemsPerPage"
      :page="results.page"
      :pages="pages"
      @setPage="setPage"
    />

    <section class="photos">
      <PhotoSearchResult
        v-for="(photo, index) in results.photos"
        :key="index"
        :photo="photo"
      />
    </section>

    <Pagination
      :itemsPerPage="results.itemsPerPage"
      :page="results.page"
      :pages="pages"
      @setPage="setPage"
    />
  </section>
</template>

<script>
import PhotoSearchResult from "./PhotoSearchResult.vue";
import Pagination from "@/components/pagination/Pagination";

export default {
  components: {
    Pagination,
    PhotoSearchResult,
  },

  props: {
    results: {
      type: Object,
      required: true,
    },
  },

  computed: {
    pages() {
      return Math.ceil(this.results.count / this.results.itemsPerPage);
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
