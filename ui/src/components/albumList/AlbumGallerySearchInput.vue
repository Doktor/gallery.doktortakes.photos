<template>
  <div class="album-search-container">
    <CustomInput
      type="text"
      label=""
      placeholder="Search albums by name"
      v-model="value"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
import CustomInput from "@/components/form/CustomInput.vue";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  modelValue: {},
});

const value = computed({
  get() {
    return props.modelValue;
  },
  set(newValue) {
    emit("update:modelValue", newValue);
  },
});
</script>

<style lang="scss" scoped>
.album-search-container {
  width: 100%;
  max-width: 500px;

  margin-bottom: 1rem;
}
</style>
