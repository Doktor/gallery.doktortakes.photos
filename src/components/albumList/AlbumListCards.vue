<template>
  <div>
    <AlbumCard
      v-for="(album, index) in albums"
      :album="album"
      :isLoading="isLoading || !album.isLoaded"
      :isVisible="isLoading ? true : indexStart <= index && index <= indexEnd"
      :key="isLoading ? index : album.path"
      :routeName="routeName"
    />
  </div>
</template>

<script>
import AlbumCard from "./AlbumCard";

export default {
  components: {
    AlbumCard,
  },

  props: {
    albums: {
      type: Array,
      required: true,
    },
    routeName: {
      type: String,
      default: "album",
    },

    indexStart: {
      type: Number,
      required: true,
    },
    indexEnd: {
      type: Number,
      required: true,
    },

    isLoading: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
