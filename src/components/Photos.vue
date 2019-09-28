<template>
  <section>
    <Pagination :mutation="'setPhotoPage'" :itemsPerPage="photosPerPage" :page="page" :pages="photoPages"/>
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
    <Pagination :mutation="'setPhotoPage'" :itemsPerPage="photosPerPage" :page="page" :pages="photoPages"/>
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
        return this.photosPerPage * (this.page - 1);
      },
      indexEnd() {
        return this.indexStart + this.photosPerPage - 1;
      },

      ...mapGetters([
        'photosPerPage',
        'photoPages',
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
