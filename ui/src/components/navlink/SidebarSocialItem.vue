<template>
  <!--  <SidebarListItem>-->
  <a
    class="sidebar-link sidebar-link-social"
    target="blank"
    rel="noopener noreferrer"
    v-bind="$attrs"
  >
    <span class="sidebar-link-social-icon">
      <slot></slot>
    </span>
    <span class="sidebar-link-social-title">{{ $attrs.title }}</span>
  </a>
  <!--  </SidebarListItem>-->
</template>

<script>
import SidebarListItem from "./SidebarListItem";

export default {
  name: "SidebarSocialItem",
  components: { SidebarListItem },
  inheritAttrs: false,
};
</script>

<style lang="scss">
.sidebar-link-social {
  display: inline-grid !important;
  justify-content: start;
  align-items: center;
  grid-template-columns: variables.$sidebar-icon-size 1fr;
  gap: 8px;

  text-decoration: none !important;

  &:hover {
    .font-awesome-circle-icon {
      color: variables.$text-color;
      background-color: variables.$background-color;
    }
  }
}

.sidebar-link-social-icon {
  i {
    display: block;
  }
}

.sidebar-link-social-title {
  @include variables.sidebar-font();
  text-decoration: underline;
}
</style>
