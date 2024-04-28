<template>
  <PaginationManager
    :isServerSide="useServerSidePagination"
    :clientSideItems="photos"
    :page="page"
    :size="size"
    :sizeOptions="sizeOptions"
    :getPage="getPage"
    @setPage="setPage"
    @setSize="setSize"
    @setItems="setItems"
  >
    <Tiles class="photo-tiles">
      <PhotoTile
        v-for="photo in items"
        :key="photo.md5"
        :allowSelect="allowSelect"
        :isSelected="
          allowSelect ? selectedPhotoHashes.includes(photo.md5) : false
        "
        :isLoading="
          useServerSidePagination ? false : isLoading || !photo.isLoaded
        "
        :isVisible="
          useServerSidePagination ? true : isLoading || photo.isLoaded
        "
        :photo="photo"
        :routeName="routeName"
        @select="select"
      />
    </Tiles>
  </PaginationManager>
</template>

<script>
import PhotoTile from "./PhotoTile";
import Tiles from "../Tiles";
import PaginationManager from "../pagination/PaginationManager";

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
      items: [],
    };
  },

  computed: {
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
    setItems(items) {
      this.items = items;
    },
  },
};
</script>

<style lang="scss">
.photo-tiles {
  grid-template-columns: repeat(auto-fit, minmax($photo-width, 1fr));
}
</style>
