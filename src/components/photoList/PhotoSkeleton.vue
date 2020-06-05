<template>
  <div>
    <div class="photo-placeholder photo-skeleton">
      <img
        :src="placeholder"
        alt="Photo thumbnail placeholder"
        title="Loading..."
      >
      <div class="note photo-no-thumbnail-note">
        <i class="fas fa-spin fa-spinner"></i>
      </div>
    </div>
  </div>
</template>

<script>
  import {staticFiles} from "../../store";


  export default {
    computed: {
      placeholder() {
        return staticFiles.squareThumbnailPlaceholder;
      },
    },
  }
</script>
