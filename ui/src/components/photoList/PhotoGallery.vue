<template>
  <PaginationManager
    v-if="useServerSidePagination || isLoading || photos.length > 0"
    :isServerSide="useServerSidePagination"
    :allItems="photos"
    :page="page"
    :size="size"
    :sizeOptions="sizeOptions"
    :getPage="getPage"
    @setPage="setPage"
    @setSize="setSize"
    @setPaginatedItems="setPaginatedItems"
  >
    <div class="photo-gallery-container">
      <Tiles class="photo-gallery">
        <PhotoTile
          v-for="n in size"
          :key="n"
          :allowSelect="allowSelect"
          :isSelected="
            allowSelect
              ? selectedPhotoHashes.includes(paginatedItems[n]?.md5)
              : false
          "
          :isLoading="loading > 0"
          :isVisible="
            useServerSidePagination ||
            loading > 0 ||
            (page - 1) * size + (n - 1) < photos.length
          "
          :photo="paginatedItems[n - 1]"
          :routeName="routeName"
          @select="select"
        />
      </Tiles>
    </div>
  </PaginationManager>
</template>

<script>
import PhotoTile from "./PhotoTile";
import Tiles from "../Tiles";
import PaginationManager from "../pagination/PaginationManager";
import { mapState } from "vuex";

export default {
  components: {
    PaginationManager,
    Tiles,
    PhotoTile,
  },

  data() {
    return {
      page: 1,
      size: 24,
      paginatedItems: [],
    };
  },

  computed: {
    ...mapState(["loading"]),
    sizeOptions() {
      return [12, 24, 48, 96];
    },
  },

  props: {
    photos: {
      type: Array,
    },
    getPage: {
      type: Function,
    },

    selectedPhotoHashes: {
      type: Array,
      default: () => [],
    },
    routeName: {
      type: String,
      default: "photo",
    },

    allowSelect: {
      type: Boolean,
      default: false,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    useServerSidePagination: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    select(md5) {
      this.$emit("select", md5);
    },

    setPage(page) {
      this.page = page;
    },
    setSize(size) {
      this.size = size;
    },
    setPaginatedItems(items) {
      this.paginatedItems = items;
    },
  },
};
</script>

<style lang="scss">
.photo-gallery-container {
  container-name: gallery;
  container-type: inline-size;
}

.photo-gallery {
  grid-template-columns: 1fr;

  @each $n in [2, 3, 4, 6, 8] {
    // Calculate the max width of (n - 1) photos with (n - 2) gaps
    $breakpoint: (variables.$photo-width * ($n - 1)) +
      (variables.$item-spacing * ($n - 2));

    // Add another column at $breakpoint + 1 so photos don't exceed $photo-width
    @container gallery (width >= #{$breakpoint + 1}) {
      grid-template-columns: repeat($n, 1fr);
    }
  }
}
</style>
