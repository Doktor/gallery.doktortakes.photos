<template>
  <SidebarListItem :showMarker="false">
    <a
      class="sidebar-link sidebar-social-item-link"
      target="blank"
      rel="noopener noreferrer"
      v-bind="$attrs"
    >
      <slot></slot>
      <span class="sidebar-social-item-title">{{ $attrs.title }}</span>
    </a>
  </SidebarListItem>
</template>

<script>
import SidebarListItem from "@/components/navlink/SidebarListItem.vue";

export default {
  name: "SidebarSocialItem",
  components: { SidebarListItem },
  inheritAttrs: false,
};
</script>

<style lang="scss">
.sidebar-social-item-link {
  display: inline-flex;
  justify-content: start;
  align-items: center;

  text-decoration: none !important;
  padding: 8px;

  width: 100%;

  &:hover {
    text-decoration: none;

    .font-awesome-circle-icon {
      color: variables.$text-color;
      background-color: variables.$background-color;
    }
  }
}

.sidebar-social-item-title {
  margin-left: 8px;

  text-decoration: underline;
}
</style>
