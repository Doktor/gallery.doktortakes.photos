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
import { useStore } from "@/store";

export default {
  props: {
    notification: {
      type: Object,
      required: true,
    },
  },

  computed: {
    classes() {
      return {
        [`notification-${this.notification.status}`]: true,
      };
    },
  },

  methods: {
    remove() {
      useStore().removeNotification(this.notification.id);
    },
  },
};
</script>

<style lang="scss">
@use "@/styles/variables";

.notification {
  @include variables.headings-font();
  color: variables.$text-color;

  border: 1px solid variables.$text-color;
  padding: 16px;

  cursor: pointer;

  &:not(:last-child) {
    margin-bottom: 1rem;
  }

  @mixin notification($color) {
    background-color: $color;
    border-color: darken($color, 20%);
  }

  &.notification-default {
    @include notification(variables.$background-color-2);
  }

  &.notification-success {
    @include notification(variables.$success-color);
  }

  &.notification-warning {
    @include notification(variables.$warning-color);
  }

  &.notification-error {
    @include notification(variables.$error-color);
  }
}
</style>
