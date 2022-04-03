<template>
  <div class="form-control">
    <label :for="id">{{ label }}</label>
    <select class="field" :id="id" :name="name" v-model="model">
      <option v-for="item in options" :value="item.value" :key="item.value">
        {{ item.display }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "CustomSelect",
  props: {
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
