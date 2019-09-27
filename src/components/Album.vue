<template>
  <div
      class="album-wrapper"
      :class="{'hidden': !this.isVisible}"
  >
    <div
        class="album"
        :class="getClasses"
    >
      <a
          :href="album.edit_url"
      >
        <img
            v-if="album.cover"
            :src="getThumbnail"
            :title="album.name"
            alt="Album cover"
        >
        <div v-else>
          <img
              :src="placeholder"
              :title="album.name"
              alt="Album cover placeholder"
          >
          <div class="note album-no-cover-note">No cover</div>
        </div>

        <div class="album-title">
          <div>{{ album.name }}</div>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
  import {staticFiles} from "../store/editAlbums";


  export default {
    computed: {
      getClasses() {
        return {
          'album-hidden': this.album.access_level > 0,
          'album-no-cover': this.album.cover === null,
        }
      },
      getThumbnail() {
        return this.isLoaded
          ? this.album.cover.thumbnail
          : this.placeholder;
      },
    },

    data() {
      return {
        placeholder: staticFiles.coverPlaceholder,
      }
    },

    props: {
      album: {
        type: Object,
        required: true,
      },

      isLoaded: {
        type: Boolean,
        required: true,
      },
      isVisible: {
        type: Boolean,
        required: true,
      },
    }
  }
</script>
