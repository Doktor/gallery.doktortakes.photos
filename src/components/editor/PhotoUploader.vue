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
        <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken" />
        <div class="fallback">
          <input type="file" name="file" />
          <input type="submit" value="Upload" />
        </div>
      </form>
    </div>
  </section>
</template>

<script>
import { getCsrfToken } from "@/utils";
import { endpoints } from "@/constants";

export default {
  data() {
    return {
      action: endpoints.albumPhotoList.replace(":path", this.path),
      csrfToken: getCsrfToken(),
    };
  },

  mounted() {
    Dropzone.autoDiscover = false;

    const dropzone = new Dropzone("#dropzone", {
      paramName: "file",
      uploadMultiple: false,
      parallelUploads: 2,
      headers: {
        Authorization: "Token " + this.$store.state.token,
      },
    });
  },

  props: {
    path: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.dropzone {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;

  border: 1px solid black;
  border-radius: 0;
}

.dz-preview {
  margin: 8px !important;
}

.dz-image {
  border-radius: 0 !important;
}
</style>
