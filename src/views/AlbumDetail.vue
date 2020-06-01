<template>
  <div v-if="!loading">
    <section class="group">
      <AlbumCover/>
      <AlbumInfo/>
    </section>

    <AlbumChildren/>

    <Photos :photos="photos" :allowSelect="false"/>
  </div>
</template>

<script>
  import {mapState} from 'vuex';

  import AlbumCard from "../components/albumList/AlbumCard.vue";
  import AlbumChildren from "../components/albumList/AlbumChildren.vue";
  import AlbumCover from "../components/albumDetail/AlbumCover.vue";
  import AlbumInfo from "../components/albumDetail/AlbumInfo.vue";
  import Photos from '../components/photoList/Photos.vue';


  export default {
    components: {
      AlbumCard,
      AlbumChildren,
      AlbumCover,
      AlbumInfo,
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

    created() {
      this.loadAlbum();
    },

    methods: {
      loadAlbum() {
        this.$store.commit('clearPhotos');
        this.$store.dispatch('getAlbum', {rawPath: this.routePath, code: this.routeAccessCode}).then(() => {
          this.$store.commit('updateDocumentTitleForAlbum');
          this.$store.commit('setPhotoPage', 1);
        });
      }
    },

    watch: {
      routePath() {
        this.loadAlbum();
      },
    },
  }
</script>
