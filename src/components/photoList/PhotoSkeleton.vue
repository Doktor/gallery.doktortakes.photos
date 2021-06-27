<template>
  <div>
    <div class="photo-placeholder photo-skeleton">
      <PhotoPlaceholder title="Loading..."/>
      <div class="note photo-no-thumbnail-note">
        <i class="fas fa-spin fa-spinner"></i>
      </div>
    </div>
  </div>
</template>

<script>
  import PhotoPlaceholder from "./PhotoPlaceholder";


  export default {
    components: {
      PhotoPlaceholder,
    },
  }
</script>
