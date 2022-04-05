<template>
  <div :class="classes" @click="remove">
    <span>{{ message }}</span>
  </div>
</template>

<script>
export default {
  computed: {
    classes() {
      return {
        message: true,
        visible: this.visible,
      };
    },
  },

  data() {
    return {
      visible: false,
    };
  },

  methods: {
    remove() {
      this.$store.commit("removeNotification", this.message);
    },
  },

  mounted() {
    setTimeout(() => (this.visible = true), 100);
  },

  props: {
    message: {
      type: String,
      required: true,
    },
  },
};
</script>
