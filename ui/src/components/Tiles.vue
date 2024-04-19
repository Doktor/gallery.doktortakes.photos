<template>
  <div class="tiles">
    <slot></slot>
  </div>
</template>

<style lang="scss">
.tiles {
  display: grid;

  column-gap: $item-spacing;
  row-gap: $item-spacing;

  margin: $item-spacing 0;
}
</style>
