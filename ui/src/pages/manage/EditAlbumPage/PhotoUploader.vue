<template>
  <section>
    <PhotoUploaderSummary :uploads="uploads" @clearSuccess="clearSuccess" />

    <section>
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

        <div class="dz-message">Drop photos here or click to upload</div>
      </form>
    </section>

    <PhotoUploaderList :uploads="uploads" />
  </section>
</template>

<script setup>
import { computed, markRaw, onBeforeUnmount, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { getCsrfToken } from "@/request";
import PhotoUploaderList from "@/pages/manage/EditAlbumPage/PhotoUploaderList.vue";
import {
  STATUS_ERROR,
  STATUS_SUCCESS,
  STATUS_UPLOADING,
} from "@/pages/manage/EditAlbumPage/uploader";
import PhotoUploaderSummary from "@/pages/manage/EditAlbumPage/PhotoUploaderSummary.vue";
import { Dropzone } from "@deltablot/dropzone";

const csrfToken = ref(getCsrfToken());
const uploads = ref([]);
const nextId = ref(0);
const dropzone = ref(null);

const store = useStore();

const props = defineProps({
  path: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["addPhoto"]);

const action = computed(() => {
  return `/api/manage/albums/${props.path}/photos/`;
});

onMounted(() => {
  Dropzone.autoDiscover = false;

  dropzone.value = new Dropzone("#dropzone", {
    paramName: "file",
    uploadMultiple: false,
    parallelUploads: 2,
    previewTemplate: "<div style='display: none'></div>",
    headers: {
      Authorization: "Token " + store.state.token,
    },
    url: action.value,
  });

  dropzone.value.on("addedfile", (file) => {
    const entry = {
      id: nextId.value,
      filename: file.name,
      size: file.size,
      thumbnailUrl: null,
      status: STATUS_UPLOADING,
      progress: 0,
      errorMessage: null,
      dzFile: markRaw(file),
    };

    nextId.value += 1;

    file.internalUploadId = entry.id;
    uploads.value.push(entry);
  });

  dropzone.value.on("thumbnail", (file, dataUrl) => {
    const entry = uploads.value.find((u) => u.id === file.internalUploadId);

    if (entry) {
      entry.thumbnailUrl = dataUrl;
    }
  });

  dropzone.value.on("uploadprogress", (file, progress) => {
    const entry = uploads.value.find((u) => u.id === file.internalUploadId);

    if (entry) {
      entry.progress = progress;
    }
  });

  dropzone.value.on("success", (file) => {
    const entry = uploads.value.find((u) => u.id === file.internalUploadId);

    if (entry) {
      entry.status = STATUS_SUCCESS;
      entry.progress = 100;
    }

    let response = JSON.parse(file.xhr.responseText);
    emit("addPhoto", response);
  });

  dropzone.value.on("error", (file, message) => {
    const entry = uploads.value.find((u) => u.id === file.internalUploadId);

    if (entry) {
      entry.status = STATUS_ERROR;

      if (Array.isArray(message)) {
        entry.errorMessage = message.join("; ");
      } else {
        entry.errorMessage = message;
      }
    }
  });
});

onBeforeUnmount(() => {
  dropzone.value.destroy();
});

function clearSuccess() {
  const completed = uploads.value.filter((u) => u.status === STATUS_SUCCESS);

  for (const entry of completed) {
    dropzone.value.removeFile(entry.dzFile);
  }

  uploads.value = uploads.value.filter((u) => u.status !== STATUS_SUCCESS);
}
</script>

<style lang="scss">
.dropzone {
  display: flex;
  justify-content: center;
  align-items: center;

  height: 192px;

  border: 2px dashed variables.$background-color-5;
  cursor: pointer;

  &:hover {
    border-color: variables.$text-blue;
  }

  .dz-message {
    @include variables.text-font();

    font-size: 1.1rem;
    color: variables.$text-color-2;
  }
}
</style>
