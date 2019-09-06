<template>
  <section>
    <h2>Upload photos</h2>

    <div id="upload">
      <form
          id="dropzone"
          class="dropzone"
          method="POST"
          enctype="multipart/form-data"
          :action="action"
      >
        <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken">
        <div class="fallback">
          <input type="file" name="files" multiple>
          <input type="submit" value="Upload">
        </div>
      </form>
    </div>
  </section>
</template>

<script>
  import {endpoints, getCsrfToken} from "../store/editAlbum";


  export default {
    data() {
      return {
        action: endpoints.albumPhotos,
        csrfToken: getCsrfToken(),
      }
    },

    mounted() {
      Dropzone.autoDiscover = false;

      const dropzone = new Dropzone("#dropzone", {
        paramName: 'files',
        parallelUploads: 3,
      });
    }
  }
</script>
