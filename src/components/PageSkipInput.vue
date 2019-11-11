<template>
  <span
      v-if="!active"
      class="page page-dots"
      @click="showInput">
    ...
  </span>
  <input
      v-else
      ref="skip"
      class="page-skip"
      title="Skip to page"
      @blur="hideInput"
      @keyup.enter="selectPage"
  >
</template>

<script>
  function isInteger(n) {
    return /^[1-9]+[0-9]?$/.test(n);
  }


  export default {
    data() {
      return {
        active: this.active,
      }
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

        this.setPage(page);
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
      setPage: {
        type: Function,
        required: true,
      },

      page: {
        type: Number,
        required: true,
      },
      pages: {
        type: Number,
        required: true,
      },
    }
  }
</script>
