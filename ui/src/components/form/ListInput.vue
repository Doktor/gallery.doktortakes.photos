<template>
  <InputWrapper :description="description" :errors="errors">
    <label :for="id">{{ label }}</label>

    <div class="list-input-wrapper">
      <div class="list-input-tags">
        <span
          v-for="(item, index) in items"
          class="list-input-item"
          :key="item"
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
.field {
  display: inline-block;
}

.list-input-input {
  border: 0;
  border-radius: 0;
  margin: 0;
  padding: 0;

  flex-grow: 1;

  &:focus,
  &:focus-visible {
    border: 0;
    outline: 0;
  }
}

.list-input-wrapper {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-wrap: wrap;

  // Style the wrapper like an input
  background-color: rgb(215, 215, 215);
  border: 1px solid rgb(195, 195, 195);
  color: rgb(40, 40, 40);

  padding: 8px;
}

.list-input-item {
  display: inline-block;

  border: 1px solid black;
  margin-right: 8px;
  margin-bottom: 8px;
  padding: 4px 8px;

  background-color: white;
  color: black;
  font-size: 14pt;

  cursor: pointer;

  &:hover {
    border-color: red;

    color: red;
    text-decoration: line-through double;
    text-decoration-color: red;
  }

  &:last-of-type {
    margin-right: 10px;
  }
}
</style>
