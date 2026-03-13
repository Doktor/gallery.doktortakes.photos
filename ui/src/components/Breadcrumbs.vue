<template>
  <nav class="breadcrumbs">
    <ul>
      <li v-for="(crumb, index) in items" :key="index">
        <router-link v-if="crumb.to" :to="crumb.to">{{
          crumb.label
        }}</router-link>
        <span v-else>{{ crumb.label }}</span>
      </li>
    </ul>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
});
</script>

<style lang="scss" scoped>
.breadcrumbs {
  margin-bottom: 16px;

  ul {
    list-style: none;
    margin: 0;
    padding: 0;

    text-align: left;
  }

  li {
    display: inline-block;

    &:not(:last-child) {
      &::after {
        content: ">";
        margin: 0 8px;
      }
    }
  }
}
</style>
