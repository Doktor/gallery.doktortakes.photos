<template>
  <Tiles v-if="album.children.length > 0" class="album-children-tiles">
    <AlbumTile
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
import AlbumTile from "@/components/albumTile/AlbumTile";
import Tiles from "@/components/Tiles";

export default {
  components: {
    Tiles,
    AlbumTile,
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

<style lang="scss">
@use "@/styles/variables";

.album-children-tiles {
  margin: 1rem 0;

  $sizes: 1, 2, 3, 4, 6, 8;

  @each $size in $sizes {
    @media (min-width: variables.$album-width * $size) {
      grid-template-columns: repeat($size, 1fr);
    }
  }
}
</style>
