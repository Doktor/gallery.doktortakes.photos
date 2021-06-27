<template>
  <div
      class="photo-wrapper"
      :class="classes"
      @click="onPhotoClicked"
  >
    <div class="photo">
      <PhotoThumbnail
        v-if="!isSkeleton"
        v-bind="{allowSelect, isLoaded, photo}"
      />
      <PhotoSkeleton v-else/>
    </div>
  </div>
</template>

<script>
  import PhotoThumbnail from "./PhotoThumbnail";
  import PhotoSkeleton from "./PhotoSkeleton";


  export default {
    components: {
      PhotoThumbnail,
      PhotoSkeleton,
    },

    computed: {
      classes() {
        return {
          hidden: !this.isVisible,
          selected: this.isSelected,
        }
      },

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
