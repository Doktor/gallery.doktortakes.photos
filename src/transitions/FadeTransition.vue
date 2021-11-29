<template>
  <transition
      name="fade"
      enter-active-class="fade-in"
      leave-active-class="fade-out"
      v-bind="$attrs"
      v-on="hooks"
  >
    <slot></slot>
  </transition>
</template>

<script>
export default {
  props: {
    duration: {
      type: Number,
      default: 1000,
    },
  },

  computed: {
    hooks() {
      const component = this;

      return {
        beforeEnter(el) {
          el.style.animationDuration = `${component.duration}ms`;
        },
        afterEnter(el) {
          el.style.animationDuration = '';
        },

        beforeLeave(el) {
          el.style.animationDuration = `${component.duration}ms`;
        },
        afterLeave(el) {
          el.style.animationDuration = '';
        },

        ...component.$listeners,
      };
    },
  },
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation-name: fade-in;
}

@keyframes fade-out {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

.fade-out {
  animation-name: fade-out;
}
</style>
