<template>
  <section>
    <Pagination
        :itemsPerPage="photosPerPage"
        :itemsPerPageChoices="itemsPerPageChoices"
        @setPage="setPhotoPage"
        @setItemsPerPage="setPhotosPerPage"
        :page="page"
        :pages="photoPages"
    />

    <section class="photos">
      <Photo
        v-for="photo in photos"
        :allowSelect="allowSelect"
        :isLoaded="isSkeleton || loaded.includes(photo.page)"
        :isSelected="allowSelect ? selected.includes(photo) : false"
        :isSkeleton="isSkeleton"
        :isVisible="isSkeleton || (indexStart <= photo.index && photo.index <= indexEnd)"
        :key="photo.md5"
        :photo="photo"
      />
    </section>

    <Pagination
        :itemsPerPage="photosPerPage"
        :itemsPerPageChoices="itemsPerPageChoices"
        @setPage="setPhotoPage"
        @setItemsPerPage="setPhotosPerPage"
        :page="page"
        :pages="photoPages"
    />
  </section>
</template>

<script>
  import Photo from './Photo.vue';
  import {mapState, mapGetters} from 'vuex';
  import Pagination from "@/components/pagination/Pagination";


  export default {
    components: {
      Pagination,
      Photo,
    },

    computed: {
      ...mapGetters([
        'photoPages',
      ]),

      ...mapState([
        'page',
        'photosPerPage',
        'loaded',
        'selected',
      ]),

      indexStart() {
        return this.photosPerPage * (this.page - 1);
      },
      indexEnd() {
        return this.indexStart + this.photosPerPage - 1;
      },

      itemsPerPageChoices() {
        return [10, 30, 60, 120];
      },
    },

    props: {
      allowSelect: {
        type: Boolean,
        default: false,
      },
      photos: {
        type: Array,
        required: true,
      },

      isSkeleton: {
        type: Boolean,
        default: false,
      },
    },

    methods: {
      setPhotoPage(page) {
        this.$store.commit('setPhotoPage', page);
      },
      setPhotosPerPage(count) {
        this.$store.commit('setPhotosPerPage', count);
      },
    },
  }
</script>
