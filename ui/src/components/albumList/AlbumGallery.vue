<template>
  <div>
    <h2 v-if="showCount" class="album-results-count">
      {{ searchResults.length }} album{{ pluralize(searchResults.length) }}
    </h2>

    <AlbumGallerySearchInput v-model="searchTerm" @input="filterAlbums" />

    <AlbumList
      v-if="loading"
      :albums="new Array(12).fill({})"
      :albumRoute="albumRoute"
      :isLoading="loading"
    />
    <AlbumList
      v-else-if="searchResults.length"
      :albums="searchResults"
      :albumRoute="albumRoute"
      :isLoading="loading"
    />
    <div v-else>No albums found.</div>
  </div>
</template>

<script>
import AlbumList from "./AlbumList";
import AlbumGallerySearchInput from "./AlbumGallerySearchInput";
import { pluralize } from "@/utils";

export default {
  components: {
    AlbumGallerySearchInput,
    AlbumList,
  },

  props: {
    loading: {
      type: Boolean,
      required: true,
    },

    albums: {
      type: Array,
      required: true,
    },

    albumRoute: {
      type: String,
      default: "album",
    },
    showCount: {
      type: Boolean,
      default: true,
    },
  },

  data() {
    return {
      searchTerm: "",
      searchResults: [],
    };
  },

  computed: {
    searchTermRegex() {
      return new RegExp(this.searchTerm, "i");
    },
  },

  methods: {
    pluralize,

    filterAlbums() {
      this.searchResults = this.searchTerm
        ? this.albums.filter(this.matchAlbum)
        : this.albums;
    },

    loadAlbums(albums) {
      this.searchResults = [...albums];
    },

    matchAlbum(album) {
      return album.name.match(this.searchTermRegex);
    },
  },

  mounted() {
    this.loadAlbums(this.albums);
  },

  watch: {
    albums(newAlbums) {
      this.loadAlbums(newAlbums);
    },
  },
};
</script>

<style lang="scss" scoped>
.album-results-count {
  text-align: left;
}
</style>
