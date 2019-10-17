<template>
  <div class="form-control">
    <label :for="'f-' + slug">{{ name }}</label>
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
