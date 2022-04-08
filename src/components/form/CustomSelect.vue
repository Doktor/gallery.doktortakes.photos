<template>
  <div class="form-control">
    <label :for="id">{{ label }}</label>
    <select class="field" :id="id" :name="name" v-model="model">
      <option v-for="item in options" :value="item.value" :key="item.value">
        {{ item.display }}
      </option>
    </select>

    <div v-if="errors.length > 0">
      <div v-for="(error, index) in errors" :key="index" class="form-error">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CustomSelect",
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
    label: {
      type: String,
      required: true,
    },
    options: {
      type: Array,
      required: true,
    },

    value: {},
  },
  computed: {
    id() {
      return `f-${this.name}`;
    },
    name() {
      return this.label.toLowerCase().replaceAll(" ", "-");
    },
    model: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
};
</script>
