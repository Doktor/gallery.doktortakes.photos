<template>
  <span
    v-if="!active"
    class="item item-thin item-page-skip-inactive"
    @click="showInput"
  >
    ...
  </span>
  <input
    v-else
    ref="skip"
    class="item item-unselectable item-page-skip-active"
    title="Skip to page"
    @blur="hideInput"
    @keyup.enter="selectPage"
  />
</template>

<script>
function isInteger(n) {
  return /^[1-9]+[0-9]?$/.test(n);
}

export default {
  data() {
    return {
      active: false,
    };
  },

  methods: {
    selectPage(event) {
      let raw = event.target.value;

      if (!isInteger(raw)) {
        return;
      }

      let page = parseInt(raw, 10);

      if (page === this.page || page < 1 || page > this.pages) {
        return;
      }

      this.$emit("setPage", page);
      this.active = false;
    },

    hideInput() {
      this.active = false;
    },
    showInput() {
      this.active = true;
      this.$nextTick(() => this.$refs.skip.focus());
    },
  },

  props: {
    page: {
      type: Number,
      required: true,
    },
    pages: {
      type: Number,
      required: true,
    },
  },
};
</script>
