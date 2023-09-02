<template>
  <main>
    <AlbumGallery :albums="albums" :showCount="false" :loading="loading" />
  </main>
</template>

<script>
import AlbumGallery from "../../components/albumList/AlbumGallery.vue";
import { AlbumService } from "../../services/AlbumService";

export default {
  components: {
    AlbumGallery,
  },

  data() {
    return {
      albums: [],
      loading: true,
    };
  },

  async created() {
    this.loading = true;
    this.albums = await AlbumService.getAllAlbums();
    this.loading = false;
  },
};
</script>
