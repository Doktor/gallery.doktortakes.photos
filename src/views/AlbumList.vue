<template>
  <main>
    <SearchAlbums :showCount="false" />
  </main>
</template>

<script>
import SearchAlbums from "@/components/albumList/SearchAlbums";

export default {
  components: {
    SearchAlbums,
  },

  async created() {
    await this.$store.dispatch("getAllAlbums");
    this.$store.commit("setAlbumsToTopLevelAlbums");
    this.$store.commit("setAlbumPage", 1);
  },
};
</script>
