<template>
  <div class="sidebar-social-item">
    <a
      class="sidebar-link sidebar-social-item-fa-wrapper"
      target="blank"
      rel="noopener noreferrer"
      v-bind="$attrs"
    >
      <slot></slot>
      <span class="sidebar-social-item-title">{{ $attrs.title }}</span>
    </a>
  </div>
</template>

<script>
export default {
  name: "SidebarSocialItem",
  inheritAttrs: false,
};
</script>

<style lang="scss" scoped>
.sidebar-social-item {
  a {
    text-decoration: none !important;
    padding: 6px;
  }
}

.sidebar-social-item-fa-wrapper {
  display: flex;
  justify-content: start;
  align-items: center;

  &:hover {
    text-decoration: none;
  }
}

.sidebar-social-item-title {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1;

  margin-left: 8px;

  text-decoration: underline;
}
</style>
