<template>
  <div class="form-control">
    <label :for="id">{{ label }}</label>

    <textarea
      v-if="type === 'textarea'"
      class="field"
      :id="id"
      :name="name"
      v-bind="$attrs"
      v-model="model"
    />
    <input
      v-else
      class="field"
      :id="id"
      :name="name"
      :type="type"
      v-bind="$attrs"
      v-model="model"
    />

    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "CustomInput",
  props: {
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: "text",
    },

    value: {
      type: String,
    },
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
