<template>
  <div
      class="photo-wrapper"
      :class="classes"
      @click="onPhotoClicked"
  >
    <div class="photo">
      <img
          v-if="photo.square_thumbnail"
          :src="getThumbnail"
          alt="Photo thumbnail"
      >
      <div v-else>
        <img
            :src="placeholder"
            alt="Photo thumbnail placeholder"
        >
        <div class="photo-no-thumbnail-note">No thumbnail</div>
      </div>
    </div>
  </div>
</template>

<script>
  import {staticFiles} from "../store/editAlbum";


  export default {
    computed: {
      classes() {
        return {
          hidden: !this.isVisible,
          selected: this.isSelected,
        }
      },

      getThumbnail() {
        return this.isLoaded
          ? this.photo.square_thumbnail
          : this.placeholder
      },
    },

    data() {
      return {
        placeholder: staticFiles.squareThumbnailPlaceholder,
      }
    },

    methods: {
      onPhotoClicked() {
        let action = this.isSelected ? 'deselectPhoto' : 'selectPhoto';
        this.$store.commit(action, this.photo);
      },
    },

    props: {
      photo: {
        type: Object,
        required: true,
      },

      isLoaded: {
        type: Boolean,
        required: true,
      },
      isSelected: {
        type: Boolean,
        required: true,
      },
      isVisible: {
        type: Boolean,
        required: true,
      },
    },
  }
</script>
