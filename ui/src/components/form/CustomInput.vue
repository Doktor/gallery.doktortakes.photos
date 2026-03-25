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
    ></textarea>
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

    <template v-for="(_, name) in $slots" :slot="name">
      <slot :name="name"></slot>
    </template>
  </InputWrapper>
</template>

<script>
import InputWrapper from "./InputWrapper";

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

    modelValue: {},
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
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>

<style lang="scss">
@use "@/styles/variables";

label {
  display: block;

  width: 100%;
  margin-bottom: 0.5rem;

  @include variables.headings-font();
  font-size: 1.5rem;
  text-align: left;
}

// elements that look like standard input elements
input,
select,
textarea,
.list-input-wrapper {
  width: 100%;

  background-color: variables.$background-color;
  border: 1px solid variables.$background-color-3;
  color: variables.$text-color;
}

// standard input elements
input,
select,
textarea {
  display: block;
  padding: 12px;

  @include variables.input-font();

  &:active,
  &:focus,
  &:focus-visible {
    outline: 2px solid variables.$text-blue;
  }

  &:disabled {
    background-color: variables.$background-color-3;
    border-color: variables.$background-color-5;

    cursor: not-allowed;
  }
}

input[type="checkbox"] {
  display: inline-block;

  width: 16px;
  height: 16px;
  margin-right: 8px;

  & + label {
    display: inline-block;

    width: unset;
    margin-bottom: 0;
  }
}
</style>
