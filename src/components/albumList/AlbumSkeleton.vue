<template>
  <div class="album-skeleton">
    <img
      :src="placeholder"
      alt="Album cover placeholder"
      title="Loading..."
    >
    <div class="note album-no-cover-note">
      <i class="fas fa-spin fa-spinner"></i>
    </div>
  </div>
</template>

<script>
  import {staticFiles} from "../../store";


  export default {
    computed: {
      placeholder() {
        return staticFiles.coverPlaceholder;
      },
    },
  }
</script>

<style lang="scss" scoped>
  .album-skeleton {
    border: 1px solid rgb(40, 40, 40);
  }
</style>
