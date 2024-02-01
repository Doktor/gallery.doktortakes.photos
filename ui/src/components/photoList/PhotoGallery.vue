<template>
  <PaginationControl
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
    <Tiles>
      <PhotoTile
        v-for="photo in items"
        :key="photo.md5"
        :allowSelect="allowSelect"
        :isSelected="
          allowSelect ? selectedPhotoHashes.includes(photo.md5) : false
        "
        :isLoading="
          useServerSidePagination
            ? false
            : isLoading || !loadedPages.includes(photo.page)
        "
        :isVisible="
          useServerSidePagination
            ? true
            : isLoading ||
              (indexStart <= photo.index && photo.index <= indexEnd)
        "
        :photo="photo"
        :routeName="routeName"
        @select="select"
      />
    </Tiles>
  </PaginationControl>
</template>

<script>
import PhotoTile from "./PhotoTile";
import Tiles from "../Tiles";
import PaginationControl from "../pagination/PaginationControl";

export default {
  components: {
    PaginationControl,
    Tiles,
    PhotoTile,
  },

  data() {
    return {
      page: 1,
      size: 12,

      items: [],
      loadedPages: [],
    };
  },

  computed: {
    indexStart() {
      return this.size * (this.page - 1);
    },
    indexEnd() {
      return this.indexStart + this.size - 1;
    },

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

    async setPage(page) {
      this.page = page;
      this.loadedPages.push(page);
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
