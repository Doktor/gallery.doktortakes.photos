<template>
  <div>
    <section class="album-cover-container">
      <AlbumCover :album="album" :isSkeleton="!!loading"/>
    </section>

    <AlbumChildren v-if="!loading" :album="album" />

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

    data() {
      return {
        album: {},
        photos: [],
      }
    },

    computed: {
      ...mapState([
        'loading',
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
        this.$store.commit('setLoading', true);

        let {ok, album, photos} = await this.$store.dispatch('getAlbumNew', {rawPath: this.routePath, code: this.routeAccessCode});

        if (!ok) {
          this.$store.commit('addNotification', "Album not found.");
          await this.$router.push({name: 'albums'});

          return;
        }

        this.album = album;
        this.photos = photos;

        this.$store.commit('updateDocumentTitleForAlbum');
        this.$store.commit('setLoading', false);
      },
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
