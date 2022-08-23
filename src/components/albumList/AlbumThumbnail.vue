<template>
  <AlbumThumbnailLoading v-if="isLoading" />

  <div v-else>
    <img
      v-if="thumbnail !== null"
      class="album-thumbnail"
      :src="thumbnail"
      :title="album.name"
      alt="Album thumbnail"
    />
    <AlbumThumbnailPlaceholder v-else :album="album" />

    <AlbumThumbnailTitle :album="album" />
  </div>
</template>

<script>
import AlbumThumbnailLoading from "@/components/albumList/AlbumThumbnailLoading";
import AlbumThumbnailPlaceholder from "@/components/albumList/AlbumThumbnailPlaceholder";
import AlbumThumbnailTitle from "@/components/albumList/AlbumThumbnailTitle";

export default {
  components: {
    AlbumThumbnailTitle,
    AlbumThumbnailPlaceholder,
    AlbumThumbnailLoading,
  },

  computed: {
    thumbnail() {
      return this.album.cover?.thumbnail?.url ?? null;
    },
  },

  props: {
    album: {
      type: Object,
      required: true,
    },

    isLoading: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.album-thumbnail {
  width: 100%;
  object-fit: cover;
}
</style>
