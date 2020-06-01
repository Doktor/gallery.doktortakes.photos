<template>
  <Pagination
      :itemsPerPage="searchResults.itemsPerPage"
      :setPage="setPage"
      :page="searchResults.page"
      :pages="pages"
  />
</template>

<script>
  import {mapState} from 'vuex';
  import Pagination from './Pagination.vue';


  export default {
    components: {
      Pagination,
    },

    computed: {
      ...mapState([
        'page',
        'searchResults',
      ]),

      pages() {
        return Math.ceil(this.searchResults.count / this.searchResults.itemsPerPage);
      },
    },

    methods: {
      setPage(page) {
        this.$store.commit('setSearchResultsPage', page);
      },
    },
  }
</script>
