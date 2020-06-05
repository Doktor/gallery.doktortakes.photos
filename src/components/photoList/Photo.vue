<template>
  <div
      class="photo-wrapper"
      :class="classes"
      @click="onPhotoClicked"
  >
    <div class="photo">
      <div
          v-if="!isSkeleton"
          :is="allowSelect ? 'div' : 'router-link'"
          :to="allowSelect ? null : photoLink"
      >
        <img
            v-if="photo.square_thumbnail"
            :src="getThumbnail"
            alt="Photo thumbnail"
        >
        <div v-else class="photo-placeholder">
          <img
              :src="placeholder"
              alt="Photo thumbnail placeholder"
          >
          <div class="photo-no-thumbnail-note">No thumbnail</div>
        </div>
      </div>
      <div v-else>
        <div class="photo-placeholder photo-skeleton">
          <img
              :src="placeholder"
              alt="Photo thumbnail placeholder"
              title="Loading..."
          >
          <div class="note photo-no-thumbnail-note">
            <i class="fas fa-spin fa-spinner"></i>
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

      photoLink() {
        return {
          name: 'photo',
          params: {
            path: this.photo.path,
            md5: this.photo.md5,
          },
          query: {
            code: this.$route.query.code,
          },
        }
      },
    },

    data() {
      return {
        placeholder: staticFiles.squareThumbnailPlaceholder,
      }
    },

    methods: {
      onPhotoClicked() {
        if (!this.allowSelect) {
          return;
        }

        let action = this.isSelected ? 'deselectPhoto' : 'selectPhoto';
        this.$store.commit(action, this.photo);
      },
    },

    props: {
      photo: {
        type: Object,
        required: true,
      },

      allowSelect: {
        type: Boolean,
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
      isSkeleton: {
        type: Boolean,
        default: false
      },
      isVisible: {
        type: Boolean,
        required: true,
      },
    },
  }
</script>
