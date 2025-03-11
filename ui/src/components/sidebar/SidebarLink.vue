<template>
  <li>
    <router-link class="sidebar-link" :title="title" :to="toComputed"
      >{{ display || title }}
    </router-link>
  </li>
</template>

<script>
export default {
  name: "SidebarLink",

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
