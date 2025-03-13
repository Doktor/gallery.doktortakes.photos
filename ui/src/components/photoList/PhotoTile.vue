<template>
  <div class="photo" :class="classes" v-show="isVisible">
    <router-link v-if="isVisible" :to="photoLink">
      <PhotoThumbnail :photo="photo" />
    </router-link>

    <div v-if="allowSelect" class="photo-select-overlay" @click="select">
      <div class="photo-select-checkbox-container">
        <input
          class="photo-select-checkbox"
          type="checkbox"
          :checked="isSelected"
        />
        <i
          v-show="isSelected"
          class="photo-select-checkbox-icon fas fa-check"
        ></i>
      </div>
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
        "photo-allow-select": this.allowSelect,
        "photo-unselected": this.allowSelect && !this.isSelected,
        "photo-selected": this.allowSelect && this.isSelected,
      };
    },

    photoLink() {
      if (this.photo === undefined) {
        return "#";
      }

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
.photo-allow-select {
  position: relative;
}

.photo-select-overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;

  cursor: pointer;

  border: 8px solid transparent;

  .photo-unselected & {
    background-color: rgba(0, 0, 0, 0.4);
  }

  .photo-selected & {
    border-color: variables.$text-blue;
  }

  &:hover,
  .photo-selected & {
    background-color: transparent;
  }

  &:hover,
  .photo-unselected &,
  .photo-selected & {
    transition: background-color ease-in-out 0.2s;
  }
}

$checkbox-size: 1.6rem;

.photo-select-checkbox-container {
  display: flex;
  justify-content: center;
  align-items: center;

  position: absolute;
  top: math.div($checkbox-size, 2);
  left: math.div($checkbox-size, 2);

  width: $checkbox-size;
  height: $checkbox-size;
}

.photo-select-checkbox {
  appearance: none;
  outline: none;

  position: absolute;
  width: 100%;
  height: 100%;

  background-color: white;
  border: 0;
  border-radius: 0;

  cursor: pointer;

  &:checked {
    background-color: variables.$text-blue;
    border: 1px solid darken(variables.$text-blue, 10%);

    cursor: pointer;
  }
}

.photo-select-checkbox-icon {
  color: white;
  z-index: 1;

  font-size: $checkbox-size * 0.65;
}
</style>
