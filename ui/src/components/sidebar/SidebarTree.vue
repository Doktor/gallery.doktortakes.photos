<template>
  <ul class="sidebar-tree">
    <li class="sidebar-tree-item" v-for="item in items" :key="item.album.path">
      <span
        v-if="item.children.length && !item.album.size"
        class="sidebar-tree-heading"
        :style="style"
      >
        {{ item.album.name }}
      </span>
      <RouterLink
        v-else
        class="sidebar-link"
        exactActiveClass="sidebar-link-active"
        :style="style"
        :title="item.album.name"
        :to="{
          name: 'featuredAlbum',
          params: { pathArray: item.album.path.split('/') },
        }"
      >
        {{ item.album.name }}
      </RouterLink>

      <SidebarTree
        v-if="item.children.length"
        :items="item.children"
        :paddingLeftPx="paddingLeftPx + increment"
      />
    </li>
  </ul>
</template>

<script setup>
import { computed } from "vue";

const increment = 16;

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  paddingLeftPx: {
    type: Number,
    default: 0,
  },
});

const style = computed(() => {
  return {
    "padding-left": `${props.paddingLeftPx}px`,
  };
});
</script>

<style lang="scss">
.sidebar-tree-item {
  margin-bottom: 32px;

  &:last-child,
  & & {
    margin-bottom: 0;
  }
}

.sidebar-tree-heading {
  display: inline-block;
  width: 100%;

  margin-bottom: 8px;

  font-weight: 700;
  font-size: 24px;
}
</style>
