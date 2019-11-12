<template>
  <section>
    <h2>{{ searchResults.count }} results</h2>

    <PaginationSearch/>

    <section class="photos">
      <PhotoSearchResult
          v-for="(photo, index) in searchResults.photos"
          :key="index"
          :photo="photo"
      />
    </section>

    <PaginationSearch/>
  </section>
</template>

<script>
  import {mapState} from 'vuex';
  import PaginationSearch from "./PaginationSearch.vue";
  import PhotoSearchResult from './PhotoSearchResult.vue';


  export default {
    components: {
      PaginationSearch,
      PhotoSearchResult,
    },

    computed: {
      ...mapState([
        'searchResults',
      ]),

      pages() {
        return Math.ceil(this.searchResults.count / this.searchResults.itemsPerPage);
      }
    },
  }
</script>

<style scoped>
  h2 {
    text-align: left;
  }
</style>
