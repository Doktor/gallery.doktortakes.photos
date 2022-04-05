<template>
  <section>
    <h2>Search all photos</h2>
    <SearchPhotoForm />
    <SearchResults />
  </section>
</template>

<script>
import SearchPhotoForm from "@/components/search/SearchPhotoForm.vue";
import SearchResults from "@/components/search/SearchResults";

export default {
  components: {
    SearchPhotoForm,
    SearchResults,
  },
};
</script>
