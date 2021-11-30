<template>
  <section>
    <Pagination
        :itemsPerPage="photosPerPage"
        :itemsPerPageChoices="itemsPerPageChoices"
        @setPage="setPage"
        @setItemsPerPage="setPhotosPerPage"
        :page="page"
        :pages="pages"
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
        @setPage="setPage"
        @setItemsPerPage="setPhotosPerPage"
        :page="page"
        :pages="pages"
    />
  </section>
</template>

<script>
  import Photo from './Photo.vue';
  import {mapState} from 'vuex';
  import Pagination from "@/components/pagination/Pagination";


  export default {
    components: {
      Pagination,
      Photo,
    },

    data() {
      return {
        photosPerPage: 10,
        page: 1,
      }
    },

    computed: {
      ...mapState([
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

      pages() {
        return Math.ceil(this.photos.length / this.photosPerPage);
      },
    },

    props: {
      photos: {
        type: Array,
        required: true,
      },

      allowSelect: {
        type: Boolean,
        default: false,
      },
      isSkeleton: {
        type: Boolean,
        default: false,
      },
    },

    methods: {
      setPage(page) {
        this.page = page;
        this.loaded.push(page);
      },

      setPhotosPerPage(count) {
        this.photosPerPage = count;

        this.photos.forEach((photo, index) => {
          photo.page = Math.floor(index / this.photosPerPage) + 1;
        });

        this.setPage(1);
      },
    },

    watch: {
      photos(newPhotos) {
        if (newPhotos.length) {
          this.setPage(1);
        }
      },
    },
  }
</script>
