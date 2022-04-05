<template>
  <ul class="album-views">
    <li>View as:</li>
    <li>
      <router-link title="Cards: default" :to="{ name: route.name, query: {} }"
        >Cards</router-link
      >
    </li>
    <li>
      <router-link
        title="Simple: text only"
        :to="{ name: route.name, query: { view: 'simple' } }"
        >Simple</router-link
      >
    </li>
    <li>
      <router-link
        title="Table"
        :to="{ name: route.name, query: { view: 'table' } }"
        >Table</router-link
      >
    </li>
  </ul>
</template>

<script>
export default {
  computed: {
    route() {
      return this.$route;
    },
  },
};
</script>

<style lang="scss" scoped>
.album-views {
  text-align: left;

  list-style-type: none;
  margin: 1rem 0;
  padding: 0;

  li {
    display: inline;

    &:not(:last-child) {
      margin-right: 16px;
    }
  }
}
</style>
