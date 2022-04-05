<template>
  <div>
    <AlbumCard
      v-for="(album, index) in albums"
      :album="album"
      :isLoaded="isSkeleton ? true : album.isLoaded"
      :isSkeleton="isSkeleton"
      :isVisible="isSkeleton ? true : indexStart <= index && index <= indexEnd"
      :key="isSkeleton ? index : album.path"
      :route="route"
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
    route: {
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

    isSkeleton: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
