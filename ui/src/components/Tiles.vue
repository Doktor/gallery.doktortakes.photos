<template>
  <div class="tiles">
    <slot></slot>
  </div>
</template>

<style lang="scss">
@use "@/styles/variables";

.tiles {
  display: grid;
  gap: variables.$item-spacing;
}
</style>
