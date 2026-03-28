<template>
  <section class="info">
    <PhotoMetadata
      class="info-metadata"
      :photo="photo"
      :count="photos.length"
    />
    <PhotoTaxa
      class="info-taxa"
      v-if="photo.taxa.length > 0"
      :taxa="photo.taxa"
    />
    <PhotoExif class="info-exif" :exif="photo.exif" />
    <PhotoLinks class="info-links" :album="album" :isExternal="isExternal" />
    <KeyboardShortcuts class="info-shortcuts" />
  </section>
</template>

<script>
import KeyboardShortcuts from "./KeyboardShortcuts";
import PhotoExif from "./PhotoExif";
import PhotoLinks from "./PhotoLinks";
import PhotoMetadata from "./PhotoMetadata";
import PhotoTaxa from "./PhotoTaxa";

export default {
  components: {
    KeyboardShortcuts,
    PhotoExif,
    PhotoLinks,
    PhotoMetadata,
    PhotoTaxa,
  },

  props: {
    album: {
      type: Object,
      required: true,
    },
    photo: {
      type: Object,
      required: true,
    },
    photos: {
      type: Array,
      required: true,
    },
    isExternal: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
<style lang="scss" scoped>
@use "@/styles/variables";

.info-shortcuts {
  display: none;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: block;
  }
}

.info {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(3, 1fr);
  gap: variables.$page-margin;

  margin: variables.$page-margin;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    grid-template-columns: 50% 50%;
    grid-template-rows: repeat(2, 1fr);

    margin: variables.$page-margin auto;
  }

  max-width: 800px;

  text-align: left;
}
</style>
