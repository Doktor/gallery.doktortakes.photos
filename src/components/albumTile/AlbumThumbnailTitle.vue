<template>
  <div class="album-thumbnail-title-container">
    <div class="album-thumbnail-title">{{ album.name }}</div>
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
  bottom: 0.5rem;
  left: 0.5rem;

  background-color: rgba($background-color, 0.8);
  border-radius: 2px;
}

.album-thumbnail-title {
  @include headings-font();

  color: $text-color;
  font-size: 1.3rem;
  line-height: 1;
  text-align: center;
  text-transform: lowercase;

  border-radius: 5px;
  margin: 0.55rem 0.65rem;

  &:hover {
    text-decoration: none;
  }

  .album-hidden & {
    color: $text-error;
  }
}
</style>
