<template>
  <section>
    <PaginationPhotos
        v-if="!isSkeleton"
        :photosPerPage="photosPerPage"
        :page="page"
        :pages="photoPages"
        @setPhotoPage="setPhotoPage"
        @setPhotosPerPage="setPhotosPerPage"
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

    <PaginationPhotos
        v-if="!isSkeleton"
        :photosPerPage="photosPerPage"
        :page="page"
        :pages="photoPages"
        @setPhotoPage="setPhotoPage"
        @setPhotosPerPage="setPhotosPerPage"
    />
  </section>
</template>

<script>
  import PaginationPhotos from '@/components/pagination/PaginationPhotos.vue';
  import Photo from './Photo.vue';
  import {mapState, mapGetters} from 'vuex';


  export default {
    components: {
      PaginationPhotos,
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
