<template>
  <div class="tiles">
    <slot></slot>
  </div>
</template>

<style lang="scss">
.tiles {
  display: flex;
  flex-wrap: wrap;

  margin: $itemSpacing (-$itemSpacing);
}
</style>
