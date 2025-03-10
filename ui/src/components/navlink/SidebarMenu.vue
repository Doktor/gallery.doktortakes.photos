<template>
  <div class="sidebar-menu-container" :class="classes">
    <div class="sidebar-menu">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "SidebarMenu",

  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    classes() {
      return {
        "sidebar-menu-open": this.isOpen,
      };
    },
  },
};
</script>

<style lang="scss">
.sidebar-menu-container {
  @media (width <= variables.$full-layout-breakpoint) {
    display: none;

    &.sidebar-menu-open {
      display: block;
    }

    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 2;

    width: 100%;
    height: 100%;
    overflow: auto;

    background-color: white;
  }

  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: block;
  }
}

.sidebar-menu {
  margin: 2rem auto 4rem auto;
  width: variables.$sidebar-width;
}
</style>
