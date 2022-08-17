<template>
  <Pagination
    :itemsPerPage="results.itemsPerPage"
    :page="results.page"
    :pages="pages"
    @setPage="setPage"
  />
</template>

<script>
import Pagination from "@/components/pagination/Pagination.vue";

export default {
  components: {
    Pagination,
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
