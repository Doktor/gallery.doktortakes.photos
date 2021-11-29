<template>
  <Pagination
      :itemsPerPage="albumsPerPage"
      :itemsPerPageChoices="itemsPerPageChoices"
      @setPage="setAlbumPage"
      @setItemsPerPage="setAlbumsPerPage"
      :page="page"
      :pages="pages"
  />
</template>

<script>
  import Pagination from './Pagination.vue';


  export default {
    components: {
      Pagination,
    },

    props: {
      albumsPerPage: {
        type: Number,
        required: true,
      },
      page: {
        type: Number,
        required: true,
      },
      pages: {
        type: Number,
        required: true,
      },
    },

    computed: {
      itemsPerPageChoices() {
        return [6, 12, 24, 48];
      },
    },

    methods: {
      setAlbumPage(page) {
        this.$emit('setAlbumPage', page);
      },
      setAlbumsPerPage(count) {
        this.$emit('setAlbumsPerPage', count);
      },
    },
  }
</script>
