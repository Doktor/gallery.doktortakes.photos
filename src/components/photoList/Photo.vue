<template>
  <div class="photo-wrapper" :class="classes">
    <div class="photo">
      <div
        :is="allowSelect ? 'div' : 'router-link'"
        :to="allowSelect ? null : photoLink"
        @click="allowSelect ? select : () => {}"
      >
        <PhotoThumbnail v-if="!isSkeleton" v-bind="{ isLoaded, photo }" />
        <PhotoSkeleton v-else />
      </div>
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
      };
    },

    photoLink() {
      return {
        name: this.route,
        params: {
          path: this.photo.path,
          md5: this.photo.md5,
        },
        query: {
          code: this.$route.query.code,
        },
      };
    },
  },

  methods: {
    select() {
      this.$emit("select", this.photo.md5);
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
    route: {
      type: String,
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
      default: false,
    },
    isVisible: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
