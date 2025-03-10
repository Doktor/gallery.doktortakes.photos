<template>
  <SidebarListItem>
    <a
      class="sidebar-link sidebar-social-link"
      target="blank"
      rel="noopener noreferrer"
      v-bind="$attrs"
    >
      <span class="sidebar-social-link-icon">
        <slot></slot>
      </span>
      <span class="sidebar-social-link-title">{{ $attrs.title }}</span>
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
.sidebar-social-link {
  display: inline-flex !important;
  justify-content: start;
  align-items: center;

  width: 100%;

  &:hover {
    .font-awesome-circle-icon {
      color: variables.$text-color;
      background-color: variables.$background-color;
    }
  }
}

.sidebar-social-link-icon {
  margin-right: variables.$sidebar-link-margin;
  text-decoration: none;
}

.sidebar-social-link-title {
  text-decoration: underline;
}
</style>
