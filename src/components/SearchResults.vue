<template>
  <section>
    <h2>{{ searchResults.count }} results</h2>

    <Pagination
        :mutation="'setSearchResultsPage'"
        :itemsPerPage="searchResults.itemsPerPage"
        :page="searchResults.page"
        :pages="pages"
    />

    <section class="photos">
      <PhotoSearchResult
          v-for="(photo, index) in searchResults.photos"
          :key="index"
          :photo="photo"
      />
    </section>

    <Pagination
        :mutation="'setSearchResultsPage'"
        :itemsPerPage="searchResults.itemsPerPage"
        :page="searchResults.page"
        :pages="pages"
    />
  </section>
</template>

<script>
  import Pagination from './Pagination.vue';
  import PhotoSearchResult from './PhotoSearchResult.vue';
  import {mapState} from 'vuex';


  export default {
    components: {
      Pagination,
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
