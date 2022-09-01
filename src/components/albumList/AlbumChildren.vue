<template>
  <Tiles v-if="album.children.length > 0">
    <AlbumCard
      v-for="child in album.children"
      :album="child"
      :isLoading="false"
      :isVisible="true"
      :key="child.path"
      :route="route"
    />
  </Tiles>
</template>

<script>
import AlbumCard from "./AlbumCard";
import Tiles from "@/components/Tiles";

export default {
  components: {
    Tiles,
    AlbumCard,
  },

  props: {
    album: {
      type: Object,
      required: true,
    },
    route: {
      type: String,
      default: "album",
    },
  },
};
</script>
