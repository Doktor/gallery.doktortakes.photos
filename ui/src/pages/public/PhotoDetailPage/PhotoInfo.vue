<template>
  <section class="info">
    <div>
      <PhotoMetadata
        class="info-metadata"
        :photo="photo"
        :count="photos.length"
      />
      <KeyboardShortcuts class="info-shortcuts" />
    </div>

    <div>
      <PhotoTaxa
        class="info-taxa"
        v-if="photo.taxa.length > 0"
        :taxa="photo.taxa"
      />
      <PhotoExif class="info-exif" :exif="photo.exif" />
      <PhotoLinks class="info-links" :album="album" />
    </div>
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
  },
};
</script>
<style lang="scss" scoped>
.info-shortcuts {
  display: none;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: block;
  }
}

.info {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  width: 90%;
  margin: 2rem auto 0 auto;
  max-width: 1000px;

  text-align: left;

  > div {
    width: 100%;

    @media (width >= variables.$full-layout-breakpoint + 1) {
      width: 50%;
    }
  }

  > div > div {
    margin-bottom: 1rem;
  }

  &::v-deep {
    dl,
    dt,
    dd {
      margin: 0;
    }

    dt,
    dd {
      display: inline;
    }
  }
}
</style>
