<template>
  <AlbumThumbnailLoading v-if="isLoading" />

  <div v-else class="album-thumbnail-container">
    <svg
      class="album-thumbnail-placeholder"
      viewBox="0 0 1 1"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect :width="1" :height="1" :fill="placeholderColor" fill-opacity="1" />
    </svg>

    <img
      v-if="thumbnail !== null"
      class="album-thumbnail"
      :class="{ 'album-thumbnail-is-loaded': isImageLoaded }"
      :style="imageStyle"
      :src="thumbnail"
      :title="album.name"
      alt="Album thumbnail"
      @load="isImageLoaded = true"
    />
    <div v-else class="album-thumbnail-no-cover">
      <span class="note album-no-cover-note">No cover</span>
    </div>

    <AlbumThumbnailTitle :album="album" />
  </div>
</template>

<script>
import AlbumThumbnailLoading from "./AlbumThumbnailLoading";
import AlbumThumbnailTitle from "./AlbumThumbnailTitle";

export default {
  components: {
    AlbumThumbnailTitle,
    AlbumThumbnailLoading,
  },

  data() {
    return {
      isImageLoaded: false,
    };
  },

  watch: {
    thumbnail() {
      this.isImageLoaded = false;
    },
  },

  computed: {
    thumbnail() {
      return this.album.cover?.thumbnail?.url ?? null;
    },
    placeholderColor() {
      let color = this.album.cover?.placeholderColor;

      if (color) {
        color = "#" + color;
      }

      return color || "white";
    },
  },

  props: {
    album: {
      type: Object,
      required: true,
    },

    isLoading: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.album-thumbnail-container {
  position: relative;
}

.album-thumbnail-placeholder {
  display: block;
}

.album-thumbnail {
  position: absolute;
  top: 0;

  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;

  opacity: 0;
  transition: opacity 0.5s ease;

  &.album-thumbnail-is-loaded {
    opacity: 1;
  }
}

.album-thumbnail-no-cover {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;

  display: flex;
  justify-content: center;
  align-content: center;

  border: 1px solid variables.$background-color-2;
}
</style>
