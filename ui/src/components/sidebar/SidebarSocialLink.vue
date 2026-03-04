<template>
  <SidebarLink class="sidebar-link-social" :href="href" :route="route" :title="title">
    <span class="sidebar-link-social-icon">
      <slot></slot>
    </span>
    <span class="sidebar-link-social-title">{{ title }}</span>
  </SidebarLink>
</template>

<script setup>
import SidebarLink from "@/components/sidebar/SidebarLink.vue";

const props = defineProps({
  href: {
    type: String,
  },
  route: {
    type: String,
  },
  title: {
    type: String,
    required: true,
  },
});
</script>

<style lang="scss">
.sidebar-link-social .sidebar-link {
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
    font-size: 24px;
  }
}

.sidebar-link-social-title {
  text-decoration: underline;
}
</style>
