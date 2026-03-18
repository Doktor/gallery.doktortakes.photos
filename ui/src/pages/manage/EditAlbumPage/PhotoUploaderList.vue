<template>
  <section v-if="uploads.length > 0" class="upload-list">
    <div v-for="upload in uploads" :key="upload.id" class="upload-row">
      <img
        v-if="upload.thumbnailUrl"
        :src="upload.thumbnailUrl"
        :title="upload.filename"
        :alt="upload.filename"
      />
      <div v-else class="thumbnail-placeholder"></div>

      <div class="upload-status">
        <div class="upload-filename">{{ upload.filename }}</div>

        <div v-if="upload.status === STATUS_UPLOADING">
          <div class="progress-bar">
            <div
              class="progress-bar-fill"
              :style="{ width: upload.progress + '%' }"
            ></div>
          </div>
          <div class="upload-status-text progress-bar-text">
            {{ Math.round(upload.progress) }}%
          </div>
        </div>
        <div
          v-else-if="upload.status === STATUS_SUCCESS"
          class="upload-status-text upload-status-success"
        >
          Success
        </div>
        <div v-else-if="upload.status === STATUS_ERROR">
          <div class="upload-status-text upload-status-error">Error</div>
          <div v-if="upload.errorMessage" class="upload-error-message">
            {{ upload.errorMessage }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import {
  STATUS_ERROR,
  STATUS_SUCCESS,
  STATUS_UPLOADING,
} from "@/pages/manage/EditAlbumPage/uploader";

defineProps({
  uploads: {
    type: Array,
    required: true,
  },
});
</script>

<style lang="scss">
$thumbnail-size: 128px;

.upload-list {
  border: 1px solid variables.$background-color-5;
}

.upload-row {
  display: grid;
  grid-template-columns: min-content 1fr;
  gap: 16px;

  padding: 16px;

  img {
    width: $thumbnail-size;
    height: $thumbnail-size;
    object-fit: cover;
  }

  .thumbnail-placeholder {
    width: $thumbnail-size;
    height: $thumbnail-size;
    background-color: variables.$background-color-3;
  }

  &:nth-child(even) {
    background-color: variables.$background-color-2;
  }
}

.upload-filename {
  @include variables.text-font();
  line-height: 1;

  margin-bottom: 16px;
}

.upload-status {
  @include variables.text-font();

  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: variables.$background-color-4;

  margin-bottom: 8px;
}

.progress-bar-fill {
  height: 100%;
  background-color: variables.$text-blue;
  transition: width 0.2s ease;
}

.progress-bar-text {
  @include variables.headings-font();
  color: variables.$text-color-2;
  line-height: 1;

  width: 64px;
}

.upload-status-text {
  @include variables.headings-font();
}

.upload-status-success {
  color: variables.$success-color;
}

.upload-status-error {
  color: variables.$error-color;
}
</style>
