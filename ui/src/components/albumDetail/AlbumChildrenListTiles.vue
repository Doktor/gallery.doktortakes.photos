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
.album-children-tiles {
  grid-template-columns: repeat(auto-fit, minmax($album-width, 1fr));
}
</style>
