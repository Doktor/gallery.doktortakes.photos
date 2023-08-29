<template>
  <Tiles v-if="album.children.length > 0">
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
import AlbumTile from "../albumTile/AlbumTile.vue";
import Tiles from "../Tiles.vue";

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
