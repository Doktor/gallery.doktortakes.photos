<template>
  <InputWrapper :description="description" :errors="errors">
    <label :for="id">{{ label }}</label>

    <select class="field" :id="id" :name="name" v-model="model">
      <option
        v-for="item in options"
        :value="item.value || item"
        :key="item.value || item"
      >
        {{ item.display || item }}
      </option>
    </select>

    <template v-for="(_, name) in $scopedSlots" :slot="name">
      <slot :name="name"></slot>
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
