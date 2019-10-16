<template>
  <div class="form-row">
    <label :for="'f-' + slug">{{ name }}</label>
    <div class="field-wrapper">
      <input
          class="field"
          :class="{'field-invalid': errors.length > 0}"
          :id="'f-' + slug"
          :name="slug"
          type="password"
          autocomplete="off"

          :value="value"
          @input="$emit('input', $event.target.value)"
      >
    </div>

    <div
        v-if="helpText"
        class="form-note"
    >
      {{ helpText }}
    </div>

    <div
        v-if="errors.length > 0"
        v-for="error in errors"
        class="form-error"
    >
      {{ error }}
    </div>
  </div>
</template>

<script>
  export default {
    computed: {
      slug() {
        return this.name.toLowerCase().replace(" ", "-");
      }
    },

    props: {
      errors: {
        type: Array,
        required: false,
      },
      helpText: {
        type: String,
        required: false,
      },
      name: {
        type: String,
        required: true,
      },
      value: {
        type: String,
      },
    }
  }
</script>

<style lang="scss" scoped>
  .field-invalid {
    border: 1px solid red;
  }

  .form-error {
    margin-top: 5px;

    color: red;
    font-size: 80%;
  }
</style>
