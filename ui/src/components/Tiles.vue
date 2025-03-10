<template>
  <div class="tiles">
    <slot></slot>
  </div>
</template>

<style lang="scss">
.tiles {
  display: grid;
  gap: variables.$item-spacing;
}
</style>
