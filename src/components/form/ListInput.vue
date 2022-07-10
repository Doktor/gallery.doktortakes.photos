<template>
  <InputWrapper :description="description" :errors="errors">
    <label :for="id">{{ label }}</label>

    <div class="list-input-wrapper">
      <span
        v-for="(item, index) in items"
        class="list-input-item"
        :key="item"
        @click="removeItem(index)"
        >{{ item }}</span
      >

      <input
        class="list-input-input"
        :class="classes"
        :id="id"
        type="text"
        v-model="current"
        @keydown.enter.prevent="addItem"
        @keydown.backspace="removeLastItem"
      />
    </div>
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

    value: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      items: [...this.value],
      current: "",
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
      if (!this.current.trim()) {
        return;
      }

      if (this.items.includes(this.current)) {
        this.current = "";
        return;
      }

      this.items.push(this.current);
      this.current = "";

      this.$emit("input", this.items);
    },
    removeItem(index) {
      this.items.splice(index, 1);
      this.$emit("input", this.items);
    },
    removeLastItem() {
      if (!this.current.trim()) {
        this.removeItem(this.items.length - 1);
        this.$emit("input", this.items);
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
  width: auto;

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

  // Style the wrapper like an input
  background-color: rgb(215, 215, 215);
  border: 1px solid rgb(195, 195, 195);
  border-radius: 4px;
  color: rgb(40, 40, 40);

  padding: 6px 8px;
}

.list-input-item {
  display: inline-block;

  border: 1px solid black;
  border-radius: 4px;
  margin-right: 6px;
  padding: 2px 6px;

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
