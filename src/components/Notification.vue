<template>
  <div
    class="notification"
    :class="classes"
    @click="remove"
    title="Click to dismiss"
  >
    {{ notification.message }}
  </div>
</template>

<script>
import { sleep } from "@/utils";

export default {
  props: {
    notification: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      visible: false,
    };
  },

  computed: {
    classes() {
      return {
        visible: this.visible,
        [this.notification.status]: true,
      };
    },
  },

  methods: {
    async remove() {
      this.visible = false;
      await sleep(200);
      this.$store.commit("removeNotification", this.notification.id);
    },
  },

  async mounted() {
    await sleep(200);
    this.visible = true;
  },
};
</script>

<style lang="scss">
.notification {
  border: 1px solid $text-color;
  color: $text-color;
  padding: 8px 16px;

  cursor: pointer;

  opacity: 0;

  &.visible {
    opacity: 1;
  }

  &,
  &.visible {
    transition: opacity 200ms ease-in-out;
  }

  &:not(:last-child) {
    margin-bottom: 1rem;
  }

  &.default {
    $color: $background-color-2;

    background-color: $color;
    border-color: darken($color, 20%);
  }

  &.success {
    $color: #00cb8a;

    background-color: $color;
    border-color: darken($color, 20%);
  }

  &.warning {
    $color: #ffea00;

    background-color: $color;
    border-color: darken($color, 20%);
  }

  &.error {
    $color: #ff5959;

    background-color: $color;
    border-color: darken($color, 20%);
  }
}
</style>
