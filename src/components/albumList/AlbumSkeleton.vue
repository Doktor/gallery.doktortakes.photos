<template>
  <div class="album-skeleton">
    <AlbumPlaceholder title="Loading..."/>
    <div class="note album-no-cover-note">
      <i class="fas fa-spin fa-spinner"></i>
    </div>
  </div>
</template>

<script>
  import AlbumPlaceholder from "./AlbumPlaceholder";


  export default {
    components: {
      AlbumPlaceholder,
    },
  }
</script>

<style lang="scss" scoped>
  .album-skeleton {
    border: 1px solid rgb(40, 40, 40);
  }
</style>
