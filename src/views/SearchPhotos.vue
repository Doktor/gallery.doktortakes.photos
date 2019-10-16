<template>
  <section>
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
