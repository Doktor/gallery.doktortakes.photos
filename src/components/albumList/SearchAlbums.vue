<template>
  <div>
    <div v-if="showCount" class="album-results-count">
      {{ results.length }} album{{ results.length | pluralize }}
    </div>

    <AlbumSearchInput v-model="search" @input="filterAlbums" />

    <Albums
      v-if="loading"
      :albums="new Array(12).fill({})"
      :albumRoute="albumRoute"
      :isSkeleton="true"
    />
    <Albums
      v-else-if="results.length"
      :albums="results"
      :albumRoute="albumRoute"
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

  props: {
    albumRoute: {
      type: String,
      default: "album",
    },
    showCount: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
    ...mapFields(["search"]),
    ...mapState(["results", "loading"]),
  },

  methods: {
    ...mapMutations(["filterAlbums"]),
  },

  filters: {
    pluralize(value) {
      return value === 1 ? "" : "s";
    },
  },
};
</script>

<style lang="scss" scoped>
.album-results-count {
  @include headings-font();
  color: $text-color;
  font-size: 2rem;
  font-weight: 400;
  line-height: 2.5rem;
  text-align: left;
  text-transform: none;

  margin: 1rem 0;
}
</style>
