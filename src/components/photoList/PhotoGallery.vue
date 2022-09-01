<template>
  <section>
    <Pagination
      :itemsPerPage="photosPerPage"
      :itemsPerPageChoices="itemsPerPageChoices"
      @setPage="setPage"
      @setItemsPerPage="setPhotosPerPage"
      :page="page"
      :pages="pages"
    />

    <Tiles>
      <PhotoTile
        v-for="photo in photos"
        :allowSelect="allowSelect"
        :isSelected="
          allowSelect ? selectedPhotoHashes.includes(photo.md5) : false
        "
        :isLoading="isLoading || !loadedPages.includes(photo.page)"
        :isVisible="
          isLoading || (indexStart <= photo.index && photo.index <= indexEnd)
        "
        :key="photo.md5"
        :photo="photo"
        :routeName="routeName"
        @select="select"
      />
    </Tiles>

    <Pagination
      :itemsPerPage="photosPerPage"
      :itemsPerPageChoices="itemsPerPageChoices"
      @setPage="setPage"
      @setItemsPerPage="setPhotosPerPage"
      :page="page"
      :pages="pages"
    />
  </section>
</template>

<script>
import PhotoTile from "./PhotoTile.vue";
import Pagination from "@/components/pagination/Pagination";
import Tiles from "@/components/Tiles";

export default {
  components: {
    Tiles,
    Pagination,
    PhotoTile,
  },

  data() {
    return {
      photosPerPage: 24,
      page: 1,
      loadedPages: [],
    };
  },

  computed: {
    indexStart() {
      return this.photosPerPage * (this.page - 1);
    },
    indexEnd() {
      return this.indexStart + this.photosPerPage - 1;
    },

    itemsPerPageChoices() {
      return [12, 24, 48, 96];
    },

    pages() {
      return Math.ceil(this.photos.length / this.photosPerPage);
    },
  },

  props: {
    photos: {
      type: Array,
      required: true,
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
  },

  mounted() {
    this.processPhotos(this.photos);
  },

  methods: {
    select(md5) {
      this.$emit("select", md5);
    },

    processPhotos(photos) {
      for (let [index, photo] of photos.entries()) {
        photo.index = index;
        photo.page = Math.floor(index / this.photosPerPage) + 1;
        photo.loaded = false;
      }

      this.setPage(1);
    },

    setPage(page) {
      this.page = page;
      this.loadedPages.push(page);
    },

    setPhotosPerPage(count) {
      this.photosPerPage = count;

      this.photos.forEach((photo, index) => {
        photo.page = Math.floor(index / this.photosPerPage) + 1;
      });

      this.setPage(1);
    },
  },

  watch: {
    photos(newPhotos) {
      if (newPhotos.length === 0) {
        return;
      }

      this.processPhotos(newPhotos);
    },
  },
};
</script>
