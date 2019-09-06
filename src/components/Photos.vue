<template>
  <section>
    <Pagination :itemsPerPage="itemsPerPage" :page="page" :pages="pages"/>
    <section class="photos">
      <Photo
          v-for="photo in photos"
          :isLoaded="loaded.includes(photo.page)"
          :isSelected="selected.includes(photo)"
          :isVisible="indexStart <= photo.index && photo.index <= indexEnd"
          :key="photo.md5"
          :photo="photo"
      ></Photo>
    </section>
    <Pagination :itemsPerPage="itemsPerPage" :page="page" :pages="pages"/>
  </section>
</template>

<script>
  import Pagination from './Pagination.vue';
  import Photo from './Photo.vue';
  import {mapGetters, mapState} from 'vuex';


  export default {
    components: {
      Pagination,
      Photo,
    },

    computed: {
      indexStart() {
        return this.itemsPerPage * (this.page - 1);
      },
      indexEnd() {
        return this.indexStart + this.itemsPerPage - 1;
      },

      ...mapGetters([
        'itemsPerPage',
        'pages',
      ]),
      ...mapState([
        'page',
        'loaded',
        'selected',
      ]),
    },

    props: {
      photos: {
        type: Array,
        required: true,
      },
    },
  }
</script>
