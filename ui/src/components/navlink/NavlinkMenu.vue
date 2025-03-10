<template>
  <li class="nav-item-with-menu" @pointerdown.prevent.stop="pointerDown">
    <div ref="opener" class="nav-item nav-menu-opener">{{ title }}</div>

    <div class="nav-menu-container" :style="menuStyles">
      <div class="nav-menu">
        <ul class="nav-menu-items">
          <slot></slot>
        </ul>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  name: "NavlinkMenu",

  data() {
    return {
      open: false,
    };
  },

  props: {
    title: {
      type: String,
      required: true,
    },
  },

  computed: {
    menuStyles() {
      return {
        display: this.open ? "block" : "none",
      };
    },
  },

  methods: {
    pointerDown(event) {
      if (event.target !== this.$refs.opener) {
        return;
      }

      if (event.button !== 0) {
        return;
      }

      this.open = !this.open;
    },
  },

  watch: {
    $route(to, from) {
      if (to !== from) {
        this.open = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.nav-item-with-menu {
  position: relative;
}

.nav-menu-opener {
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }
}

.nav-menu-container {
  display: none;
  position: absolute;
  z-index: 1000;

  left: 50%;
  transform: translate(-50%, -0.75rem);
}

.nav-menu {
  border: 1px solid variables.$text-color;
  padding: 0.5rem;

  background-color: variables.$background-color;
}

.nav-menu-items {
  list-style-type: none;

  margin: 0;
  padding: 0;

  .nav-item {
    margin: 0 1rem;
    z-index: 1000;

    text-align: center;
    white-space: nowrap;
  }

  .nav-item-link {
    color: variables.$text-color;
  }
}
</style>
