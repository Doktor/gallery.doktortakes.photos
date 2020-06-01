<template>
  <div
      class="album-wrapper"
      :class="{'hidden': !isSkeleton && !isVisible}"
  >
    <div
        class="album"
        :class="albumClasses"
    >
      <div
          :is="isSkeleton ? 'div' : 'router-link'"
          :to="isSkeleton ? null : {name: route, params: {path: album.pathSplit}}"
      >
        <div>
          <template v-if="!isSkeleton">
            <!-- Album loaded -->
            <img
                v-if="album.cover"
                :src="thumbnail"
                :title="album.name"
                alt="Album cover"
            >
            <!-- Album loaded, no cover image -->
            <div v-else>
              <img
                  :src="placeholder"
                  :title="album.name"
                  alt="Album cover placeholder"
              >
              <div class="note album-no-cover-note">No cover</div>
            </div>
          </template>
          <!-- Skeleton -->
          <div
              v-else
              class="album-cover-placeholder"
              :class="albumCoverSkeletonClasses"
          >
            <img
                :src="placeholder"
                alt="Album cover placeholder"
                title="Loading..."
            >
            <div class="note album-no-cover-note">
              <i class="fas fa-spin fa-spinner"></i>
            </div>
          </div>

          <div class="album-title">
            <div class="album-title-text loading">{{ album.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {staticFiles} from "../../store";


  export default {
    computed: {
      albumClasses() {
        return {
          'album-hidden': this.album.access_level > 0,
          'album-no-cover': this.album.cover === null,
        }
      },

      albumCoverSkeletonClasses() {
        return {
          'loading': this.isSkeleton,
        }
      },

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

      index: {
        type: Number,
        required: true,
      },

      isLoaded: {
        type: Boolean,
        default: false,
      },
      isSkeleton: {
        type: Boolean,
        default: false,
      },
      isVisible: {
        type: Boolean,
        required: true,
      },
    }
  }
</script>

<style lang="scss" scoped>
  .album-title-text.loading {
    height: 1.1rem;
  }

  .album-cover-placeholder {
    position: relative;

    &.loading {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
</style>
