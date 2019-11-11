<template>
  <Pagination
      :itemsPerPage="photosPerPage"
      :itemsPerPageChoices="itemsPerPageChoices"
      :setItemsPerPage="setItemsPerPage"
      :mutation="'setPhotoPage'"
      :page="page"
      :pages="photoPages"
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
        'photoPages',
      ]),
      ...mapState([
        'photosPerPage',
        'page',
      ]),

      itemsPerPageChoices() {
        return [10, 30, 60, 120];
      },
    },

    methods: {
      setItemsPerPage(count) {
        this.$store.commit('setPhotosPerPage', count);
      },
    },
  }
</script>
