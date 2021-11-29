<template>
  <Pagination
      :itemsPerPage="photosPerPage"
      :itemsPerPageChoices="itemsPerPageChoices"
      @setPage="setPhotoPage"
      @setItemsPerPage="setPhotosPerPage"
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
      photosPerPage: {
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
        return [10, 30, 60, 120];
      },
    },

    methods: {
      setPhotoPage(page) {
        this.$emit('setPhotoPage', page);
      },
      setPhotosPerPage(count) {
        this.$emit('setPhotosPerPage', count);
      },
    },
  }
</script>
