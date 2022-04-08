<template>
  <FixedWidthContainer v-if="!loading">
    <section>
      <h2>Recently updated albums</h2>

      <Albums v-if="albums.length" :albums="albums" :albumRoute="'album'" />
      <div v-else>No albums found.</div>
    </section>
  </FixedWidthContainer>
</template>

<script>
import { mapState } from "vuex";
import Albums from "@/components/albumList/Albums";
import Photos from "@/components/photoList/Photos.vue";
import FixedWidthContainer from "@/components/FixedWidthContainer";

export default {
  components: {
    Albums,
    FixedWidthContainer,
    Photos,
  },

  computed: {
    ...mapState(["albums", "loading"]),
  },

  created() {
    this.$store.dispatch("getRecent");
  },
};
</script>

<style scoped>
section:not(:last-child) {
  margin-bottom: 3rem;
}
</style>
