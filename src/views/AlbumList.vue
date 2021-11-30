<template>
  <main>
    <SearchAlbums :albums="albums" :showCount="false" :loading="loading" />
  </main>
</template>

<script>
import SearchAlbums from "@/components/albumList/SearchAlbums";

export default {
  components: {
    SearchAlbums,
  },

  data() {
    return {
      albums: [],
      loading: true,
    }
  },

  async created() {
    this.loading = true;

    let albums = await this.$store.dispatch("getAllAlbums");
    this.albums = albums.filter(album => album.parent === null);

    this.loading = false;
  },
};
</script>
