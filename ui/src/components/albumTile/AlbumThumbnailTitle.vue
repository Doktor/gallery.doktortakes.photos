<template>
  <div class="album-thumbnail-title-container">
    <div class="album-thumbnail-title" :title="album.name">
      {{ album.name }}
    </div>
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
@use "@/styles/variables";

.album-thumbnail-title-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;

  background-color: rgba(black, 0.5);
}

.album-thumbnail-title {
  @include variables.headings-font();

  color: variables.$background-color;
  font-size: 1.3rem;
  text-align: left;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  padding: 12px;

  &:hover {
    text-decoration: none;
  }

  .album-hidden & {
    color: variables.$text-error;
  }
}
</style>
