<template>
  <InputWrapper :description="description" :errors="errors">
    <label :for="id">{{ label }}</label>

    <div class="list-input-wrapper">
      <div class="list-input-items">
        <span
          v-for="(item, index) in items"
          class="list-input-item"
          :key="item"
          title="Click to delete"
          @click="removeItem(index)"
          >{{ item }}</span
        >
      </div>

      <input
        class="list-input-input"
        :class="classes"
        :id="id"
        type="text"
        v-model="inputValue"
        @keydown.enter.prevent="addItem"
        @keydown.backspace="removeLastItem"
      />
    </div>
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

    modelValue: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      items: [...this.modelValue],
      inputValue: "",
    };
  },

  computed: {
    classes() {
      return {
        "field-invalid": this.errors.length > 0,
      };
    },
    id() {
      return `f-${this.name}`;
    },
    name() {
      return this.label.toLowerCase().replaceAll(" ", "-");
    },
  },

  methods: {
    addItem() {
      if (!this.inputValue.trim()) {
        return;
      }

      if (this.items.includes(this.inputValue)) {
        this.inputValue = "";
        return;
      }

      this.items.push(this.inputValue);
      this.inputValue = "";

      this.$emit("update:modelValue", this.items);
    },

    removeItem(index) {
      this.items.splice(index, 1);
      this.$emit("update:modelValue", this.items);
    },

    removeLastItem() {
      if (!this.inputValue.trim()) {
        this.removeItem(this.items.length - 1);
        this.$emit("update:modelValue", this.items);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@use "@/styles/variables";

.list-input-wrapper {
  padding: 0;

  input {
    border: 0;
  }

  &:focus-within {
    outline: 2px solid variables.$text-blue;

    input {
      &:active,
      &:focus,
      &:focus-visible {
        outline: 0;
      }
    }
  }
}

.list-input-items {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 8px;

  padding: 8px;

  background-color: variables.$background-color-3;

  text-align: left;
}

.list-input-item {
  border: 1px solid black;
  padding: 4px 8px;

  background-color: variables.$background-color;
  color: variables.$text-color;
  font-size: 1.2rem;

  cursor: pointer;

  &:hover {
    border-color: red;

    color: red;
    text-decoration: line-through;
    text-decoration-color: red;
  }
}
</style>
