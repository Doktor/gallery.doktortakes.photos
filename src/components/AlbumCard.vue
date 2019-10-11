<template>
  <div
      class="album-wrapper"
      :class="{'hidden': !this.isVisible}"
  >
    <div
        class="album"
        :class="classes"
    >
      <router-link
          :to="{name: route, params: {path: album.path}}"
      >
        <img
            v-if="album.cover"
            :src="thumbnail"
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
      </router-link>
    </div>
  </div>
</template>

<script>
  import {staticFiles} from "../store/editor";


  export default {
    computed: {
      classes() {
        return {
          'album-hidden': this.album.access_level > 0,
          'album-no-cover': this.album.cover === null,
        }
      },

      thumbnail() {
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
      route: {
        type: String,
        default: "album",
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
