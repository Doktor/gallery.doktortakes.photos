<template>
  <div class="photo-wrapper">
    <slot></slot>
  </div>
</template>

<style lang="scss">
$photoWidth: 300px;

.photo-wrapper {
  padding: $itemSpacing;

  @media (max-width: $photoWidth * 1) {
    width: 100%;
  }
  @for $i from 1 through 4 {
    @media (min-width: $photoWidth * ($i) + 1) and (max-width: $photoWidth * ($i + 1)) {
      width: math.div(100%, $i + 1); // 50%, 33%, 25%, 20%
    }
  }
  @media (min-width: $photoWidth * 5 + 1) {
    width: math.div(100%, 6);
  }

  @include fade();
}
</style>
