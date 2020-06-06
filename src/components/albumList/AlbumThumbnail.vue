<template>
  <router-link :to="{name: route, params: {path: album.pathSplit}}">
    <!-- Cover image exists -->
    <img
      v-if="album.cover"
      :src="thumbnail"
      :title="album.name"
      alt="Album cover"
    >
    <!-- No cover image -->
    <div v-else>
      <img
        :src="placeholder"
        :title="album.name"
        alt="Album cover placeholder"
      >
      <div class="note album-no-cover-note">No cover</div>
    </div>

    <div class="album-title">
      <div class="album-title-text">{{ album.name }}</div>
    </div>
  </router-link>
</template>

<script>
  import {staticFiles} from "../../store";


  export default {
    computed: {
      placeholder() {
        return staticFiles.coverPlaceholder;
      },

      thumbnail() {
        return this.isLoaded
          ? this.album.cover.thumbnail
          : this.placeholder;
      },
    },

    props: {
      album: {
        type: Object,
        required: true,
      },

      route: {
        type: String,
        default: "album",
      },

      isLoaded: {
        type: Boolean,
        default: false,
      },
    },
  }
</script>

<style lang="scss" scoped>
  .album-title-text {
    &:hover {
      text-decoration: none;
    }
  }
</style>
