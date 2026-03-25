<template>
  <hr class="sidebar-divider" />
</template>

<style lang="scss">
@use "@/styles/variables";

.sidebar-divider {
  margin: variables.$sidebar-margin 0;
  border: 0;
  border-top: 8px solid variables.$text-color;

  width: variables.$sidebar-width;
}
</style>
