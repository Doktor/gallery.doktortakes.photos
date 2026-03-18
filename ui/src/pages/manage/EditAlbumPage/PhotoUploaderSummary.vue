<template>
  <section v-if="uploads.length > 0" class="upload-summary">
    <span>{{ uploads.length }} file{{ pluralize(uploads.length) }}</span>
    <span v-if="counts.uploading > 0" class="upload-summary-count-uploading">
      {{ counts.uploading }} uploading
    </span>
    <span v-if="counts.success > 0" class="upload-summary-count-success">
      {{ counts.success }} success
    </span>
    <span v-if="counts.error > 0" class="upload-summary-count-error">
      {{ counts.error }} error
    </span>

    <CustomButton
      class="upload-summary-clear-success"
      v-if="counts.success > 0"
      @click="emit('clearSuccess')"
    >
      Clear successful uploads
    </CustomButton>
  </section>
</template>

<script setup>
import CustomButton from "@/components/form/CustomButton.vue";
import { computed } from "vue";
import { pluralize } from "@/utils";
import {
  STATUS_ERROR,
  STATUS_SUCCESS,
  STATUS_UPLOADING,
} from "@/pages/manage/EditAlbumPage/uploader";

const emit = defineEmits(["clearSuccess"]);

const { uploads } = defineProps({
  uploads: {
    type: Array,
    required: true,
  },
});

const counts = computed(() => {
  return {
    uploading: uploads.filter((u) => u.status === STATUS_UPLOADING).length,
    success: uploads.filter((u) => u.status === STATUS_SUCCESS).length,
    error: uploads.filter((u) => u.status === STATUS_ERROR).length,
  };
});
</script>

<style lang="scss">
.upload-summary {
  @include variables.headings-font();

  display: flex;
  align-items: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.upload-summary-count-uploading {
  color: variables.$text-blue;
}

.upload-summary-count-success {
  color: variables.$success-color;
}

.upload-summary-count-error {
  color: variables.$error-color;
}

.upload-summary-clear-success {
  margin-left: auto;
}
</style>
