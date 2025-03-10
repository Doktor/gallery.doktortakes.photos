<template>
  <div class="nav-item-social">
    <a
      class="nav-item-link nav-item-fa-wrapper"
      target="blank"
      rel="noopener noreferrer"
      v-bind="$attrs"
    >
      <slot></slot>
      <span class="nav-link-title">{{ $attrs.title }}</span>
    </a>
  </div>
</template>

<script>
export default {
  name: "NavlinkSocial",
  inheritAttrs: false,
};
</script>

<style lang="scss" scoped>
.nav-item-social {
  a {
    text-decoration: none !important;
    padding: 6px;
  }
}

.nav-item-fa-wrapper {
  display: flex;
  justify-content: start;
  align-items: center;

  &:hover {
    text-decoration: none;
  }
}

.nav-link-title {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1;

  margin-left: 8px;

  text-decoration: underline;
}
</style>
