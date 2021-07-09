<template>
  <div>
    <section class="album-cover-container">
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

  import AlbumCard from "@/components/albumList/AlbumCard";
  import AlbumChildren from "@/components/albumList/AlbumChildren";
  import AlbumCover from "@/components/albumDetail/AlbumCover";
  import Photos from '@/components/photoList/Photos.vue';


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

        let ok = await this.$store.dispatch('getAlbum', {rawPath: this.routePath, code: this.routeAccessCode});

        if (!ok) {
          this.$store.commit('addNotification', "Album not found.");
          this.$router.push({name: 'albums'});

          this.$store.commit('setLoading', false);
          return;
        }

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

<style scoped>
.album-cover-container {
  margin: 0;
}
</style>
