<template>
  <section>
    <h2>Search all photos</h2>
    <SearchPhotoForm/>
    <SearchResults/>
  </section>
</template>

<script>
  import SearchPhotoForm from '../components/SearchPhotoForm.vue';
  import SearchResults from "../components/SearchResults.vue";


  export default {
    components: {
      SearchPhotoForm,
      SearchResults,
    },
  }
</script>
