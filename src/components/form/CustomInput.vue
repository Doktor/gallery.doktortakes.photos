<template>
  <InputWrapper :description="description" :errors="errors">
    <label v-if="type !== 'checkbox'" :for="id">{{ label }}</label>

    <textarea
      v-if="type === 'textarea'"
      :class="classes"
      :id="id"
      :name="name"
      v-bind="$attrs"
      v-model="model"
    />
    <input
      v-else
      :class="classes"
      :id="id"
      :name="name"
      :type="type"
      v-bind="$attrs"
      v-model="model"
    />

    <label v-if="type === 'checkbox'" :for="id">{{ label }}</label>

    <template v-for="(_, name) in $scopedSlots" :slot="name">
      <slot :name="name" />
    </template>
  </InputWrapper>
</template>

<script>
import InputWrapper from "@/components/form/InputWrapper";

export default {
  components: { InputWrapper },
  props: {
    description: {
      type: String,
      required: false,
    },
    errors: {
      type: Array,
      default: () => [],
    },
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: "text",
    },

    value: {},
  },
  computed: {
    classes() {
      return {
        "field": true,
        "field-invalid": this.errors.length > 0,
      };
    },
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

<style lang="scss" scoped>
.field[type="checkbox"] {
  width: 16px;
  height: 16px;

  margin-right: 8px;

  vertical-align: 2px;

  & + label {
    display: inline;
    width: auto;
  }
}
</style>
