<template>
  <section>
    <h2>Upload photos</h2>

    <CustomInput label="Add watermark" type="checkbox" v-model="addWatermark" />

    <div>
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
import { getCsrfToken, getQueryString } from "@/utils";
import { endpoints } from "@/constants";
import CustomInput from "../form/CustomInput.vue";

export default {
  components: { CustomInput },

  data() {
    return {
      addWatermark: true,
      csrfToken: getCsrfToken(),
    };
  },

  computed: {
    action() {
      let base = endpoints.manageAlbumPhotoList.replace(":path", this.path);
      let options = {};

      if (this.addWatermark) {
        options.addWatermark = true;
      }

      return base + getQueryString(options);
    },
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
