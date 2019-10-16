<template>
  <section>
    <h2>{{ searchResults.count }} results</h2>

    <Pagination
        :mutation="'setSearchResultsPage'"
        :itemsPerPage="photosPerPage"
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
        :itemsPerPage="photosPerPage"
        :page="searchResults.page"
        :pages="pages"
    />
  </section>
</template>

<script>
  import Pagination from './Pagination.vue';
  import PhotoSearchResult from './PhotoSearchResult.vue';
  import {mapGetters, mapState} from 'vuex';


  export default {
    components: {
      Pagination,
      PhotoSearchResult,
    },

    computed: {
      ...mapGetters([
        'photosPerPage',
      ]),
      ...mapState([
        'searchResults',
      ]),

      pages() {
        return Math.floor(this.searchResults.count / this.photosPerPage);
      }
    },
  }
</script>

<style scoped>
  h2 {
    text-align: left;
  }
</style>
