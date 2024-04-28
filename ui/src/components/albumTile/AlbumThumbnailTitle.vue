<template>
  <div class="album-thumbnail-title-container">
    <div class="album-thumbnail-title" :title="album.name">{{ album.name }}</div>
  </div>
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

<style lang="scss">
.album-thumbnail-title-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;

  background-color: rgba(black, 0.5);
}

.album-thumbnail-title {
  @include headings-font();

  color: $background-color;
  font-size: 1.3rem;
  line-height: 1;
  text-align: left;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  padding: 12px;

  &:hover {
    text-decoration: none;
  }

  .album-hidden & {
    color: $text-error;
  }
}
</style>
