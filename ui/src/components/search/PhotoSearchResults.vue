<template>
  <section>
    <h2>{{ results.count }} results</h2>

    <Pagination
      :itemsPerPage="results.itemsPerPage"
      :page="results.page"
      :pages="pages"
      @setPage="setPage"
    />

    <Tiles>
      <PhotoTile
        v-for="(photo, index) in results.photos"
        :allowSelect="false"
        :key="index"
        :photo="photo"
        routeName="photo"
        :isLoading="false"
        :isVisible="true"
      />
    </Tiles>

    <Pagination
      :itemsPerPage="results.itemsPerPage"
      :page="results.page"
      :pages="pages"
      @setPage="setPage"
    />
  </section>
</template>

<script>
import Pagination from "../pagination/Pagination";
import PhotoTile from "../photoList/PhotoTile";
import Tiles from "../Tiles";

export default {
  components: {
    Tiles,
    PhotoTile,
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

<style scoped>
h2 {
  text-align: left;
}
</style>
