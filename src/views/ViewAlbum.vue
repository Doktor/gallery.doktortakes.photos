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

  import AlbumCard from "../components/AlbumCard.vue";
  import AlbumChildren from "../components/AlbumChildren.vue";
  import AlbumCover from "../components/AlbumCover.vue";
  import AlbumInfo from "../components/AlbumInfo.vue";
  import Photos from '../components/Photos.vue';


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
        this.$store.dispatch('getAlbum', this.routePath).then(() => {
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
