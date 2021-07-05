<template>
  <div>
    <AlbumSearchInput v-model="search" @input="filterAlbums" />

    <Albums
      v-if="loading"
      :albums="new Array(12).fill({})"
      :albumRoute="'album'"
      :isSkeleton="true"
    />
    <Albums
      v-else-if="results.length"
      :albums="results"
      :albumRoute="'album'"
    />
    <div v-else>No albums found.</div>
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import { mapFields } from "vuex-map-fields";
import Albums from "@/components/albumList/Albums";
import AlbumSearchInput from "@/components/albumList/AlbumSearchInput.vue";

export default {
  components: {
    AlbumSearchInput,
    Albums,
  },

  computed: {
    ...mapFields(["search"]),
    ...mapState(["results", "loading"]),
  },

  methods: {
    ...mapMutations(["filterAlbums"]),
  },
};
</script>
