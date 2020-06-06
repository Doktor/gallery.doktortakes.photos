<template>
  <div>
    <section class="group">
      <AlbumCover :isSkeleton="!!loading"/>
    </section>

    <AlbumChildren v-if="!loading"/>

    <Photos
      v-if="loading"
      :photos="new Array(12).fill({})"
      :allowSelect="false"
      :isSkeleton="true"
    />
    <Photos
      v-else-if="photos.length > 0"
      :photos="photos"
      :allowSelect="false"
    />
  </div>
</template>

<script>
  import {mapState} from 'vuex';

  import AlbumCard from "../components/albumList/AlbumCard.vue";
  import AlbumChildren from "../components/albumList/AlbumChildren.vue";
  import AlbumCover from "../components/albumDetail/AlbumCover.vue";
  import Photos from '../components/photoList/Photos.vue';


  export default {
    components: {
      AlbumCard,
      AlbumChildren,
      AlbumCover,
      Photos,
    },

    computed: {
      ...mapState([
        'album',
        'loading',
        'photos',
      ]),

      routeAccessCode() {
        return this.$route.query.code || "";
      },

      routePath() {
        return this.$route.params.path;
      },
    },

    async created() {
      await this.loadAlbum();
    },

    methods: {
      async loadAlbum() {
        this.$store.commit('clearPhotos');

        await this.$store.dispatch('getAlbum', {rawPath: this.routePath, code: this.routeAccessCode});

        this.$store.commit('updateDocumentTitleForAlbum');
        this.$store.commit('setPhotoPage', 1);
      }
    },

    watch: {
      async routePath() {
        await this.loadAlbum();
      },
    },
  }
</script>
