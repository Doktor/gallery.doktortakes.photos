<template>
  <Pagination
      :itemsPerPage="albumsPerPage"
      :itemsPerPageChoices="itemsPerPageChoices"
      :setItemsPerPage="setItemsPerPage"
      :mutation="'setAlbumPage'"
      :page="page"
      :pages="albumPages"
  />
</template>

<script>
  import {mapGetters, mapState} from 'vuex';
  import Pagination from './Pagination.vue';


  export default {
    components: {
      Pagination,
    },

    computed: {
      ...mapGetters([
        'albumPages',
      ]),
      ...mapState([
        'albumsPerPage',
        'page',
      ]),

      itemsPerPageChoices() {
        return [6, 12, 24, 48];
      },
    },

    methods: {
      setItemsPerPage(count) {
        this.$store.commit('setAlbumsPerPage', count);
      },
    },
  }
</script>
