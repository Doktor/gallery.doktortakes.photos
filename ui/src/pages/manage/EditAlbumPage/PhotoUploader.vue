<template>
  <section>
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
import { getQueryString, wait } from "@/utils";
import CustomInput from "@/components/form/CustomInput";
import { getCsrfToken } from "@/request";

export default {
  components: { CustomInput },

  data() {
    return {
      csrfToken: getCsrfToken(),
    };
  },

  computed: {
    action() {
      let base = `/api/manage/albums/${this.path}/photos/`;
      let options = {};

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

    dropzone.on("success", (file) => {
      let response = JSON.parse(file.xhr.responseText);
      this.$emit("addPhoto", response);

      wait(2000, () => {
        dropzone.removeFile(file);
      });
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
