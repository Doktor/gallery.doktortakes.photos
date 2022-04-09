<template>
  <img
    class="album-cover-image"
    alt="Cover photo"
    :src="album.cover.thumbnail.url"
    :title="album.name"
  />
</template>

<script>
export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.album-cover-image {
  position: absolute;
  z-index: 0;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;

  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
