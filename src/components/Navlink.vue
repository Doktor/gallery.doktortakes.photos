<template>
  <li class="nav-item">
    <router-link class="nav-item-link" :title="title" :to="toComputed"
      >{{ display || title }}
    </router-link>
  </li>
</template>

<script>
export default {
  name: "Navlink",

  props: {
    title: {
      type: String,
      required: true,
    },
    display: {
      type: String,
      default: "",
    },
    route: {
      type: String,
    },
    to: {
      type: Object,
    },
  },

  computed: {
    toComputed() {
      if (this.to !== undefined) {
        return this.to;
      }

      return { name: this.route };
    },
  },
};
</script>
