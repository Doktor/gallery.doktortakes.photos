<template>
  <div class="photo-wrapper" :class="classes">
    <div class="photo">
      <component
        :is="allowSelect || photo.path === undefined ? 'div' : 'router-link'"
        :to="allowSelect ? null : photoLink"
        @click="select"
      >
        <PhotoThumbnail :isLoading="isLoading" :photo="photo" />
      </component>
    </div>
  </div>
</template>

<script>
import PhotoThumbnail from "./PhotoThumbnail";

export default {
  components: {
    PhotoThumbnail,
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
    routeName: {
      type: String,
      required: true,
    },

    isSelected: {
      type: Boolean,
      default: false,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    isVisible: {
      type: Boolean,
      required: true,
    },
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
        name: this.routeName,
        params: {
          path: this.photo.path?.split("/") ?? "",
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
      if (!this.allowSelect) {
        return;
      }

      this.$emit("select", this.photo.md5);
    },
  },
};
</script>

<style lang="scss">
$photoWidth: 300px;

.photo-wrapper {
  padding: $itemSpacing;

  @media (max-width: $photoWidth * 1) {
    width: 100%;
  }
  @for $i from 1 through 4 {
    @media (min-width: $photoWidth * ($i) + 1) and (max-width: $photoWidth * ($i + 1)) {
      width: math.div(100%, $i + 1); // 50%, 33%, 25%, 20%
    }
  }
  @media (min-width: $photoWidth * 5 + 1) {
    width: math.div(100%, 6);
  }

  &.empty {
    padding: 0;
  }

  &.selected img {
    filter: brightness(0.3);
  }

  @include fade();
}
</style>
