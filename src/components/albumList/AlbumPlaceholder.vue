<template>
  <img
    :src="placeholder"
    alt="Album cover placeholder"
  >
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
