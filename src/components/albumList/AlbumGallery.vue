<template>
  <div>
    <div v-if="showCount" class="album-results-count">
      {{ searchResults.length }} album{{ searchResults.length | pluralize }}
    </div>

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
import AlbumList from "@/components/albumList/AlbumList";
import AlbumGallerySearchInput from "@/components/albumList/AlbumGallerySearchInput.vue";

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
