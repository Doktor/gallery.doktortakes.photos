<template>
  <div class="album-wrapper" :class="wrapperClasses">
    <div class="album" :class="classes">
      <component
        :is="isLoading ? 'div' : 'router-link'"
        :to="isLoading ? null : albumLink"
      >
        <AlbumThumbnail :isLoading="isLoading" :album="album" />
      </component>
    </div>
  </div>
</template>

<script>
import AlbumThumbnail from "./AlbumThumbnail";

export default {
  components: {
    AlbumThumbnail,
  },

  computed: {
    classes() {
      return {
        "album-hidden": this.album.access_level > 0,
        "album-no-cover": this.album.cover === null,
      };
    },
    wrapperClasses() {
      return {
        hidden: !this.isSkeleton && !this.isVisible,
      };
    },

    albumLink() {
      return {
        name: this.routeName,
        params: {
          path: this.album.pathSplit,
        },
      };
    },
  },

  props: {
    album: {
      type: Object,
      required: true,
    },

    routeName: {
      type: String,
      default: "album",
    },

    isLoading: {
      type: Boolean,
      required: true,
    },
    isVisible: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style lang="scss">
$albumWidth: 400px;

.album-wrapper {
  padding: $itemSpacing;

  @media (max-width: $albumWidth * 2) {
    width: 100%;
  }
  @media (min-width: $albumWidth * 2 + 1) and (max-width: $albumWidth * 3) {
    width: math.div(100%, 2); // 50%
  }
  @media (min-width: $albumWidth * 3 + 1) and (max-width: $albumWidth * 4) {
    width: math.div(100%, 3); // 33%
  }
  @media (min-width: $albumWidth * 4 + 1) and (max-width: $albumWidth * 6) {
    width: math.div(100%, 4); // 25%
  }
  @media (min-width: $albumWidth * 6 + 1) {
    width: math.div(100%, 6); // 16.67%
  }

  @include fade();
}

.album {
  position: relative;
}
</style>
