<template>
  <div class="form-control">
    <slot></slot>

    <div v-if="description" class="form-note">
      {{ description }}
    </div>

    <div v-if="errors.length > 0">
      <div v-for="(error, index) in errors" :key="index" class="form-error">
        {{ error }}
      </div>
    </div>

    <slot name="footer"></slot>
  </div>
</template>

<script>
export default {
  props: {
    description: {
      type: String,
      required: false,
    },
    errors: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
