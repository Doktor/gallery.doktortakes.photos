<template>
  <img
    :src="placeholder"
    alt="Photo thumbnail placeholder"
  >
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
