<template>
  <div class="album-wrapper">
    <slot></slot>
  </div>
</template>

<style lang="scss">
$albumWidth: 400px;

.album-wrapper {
  padding: $itemSpacing;

  @media (max-width: $albumWidth * 2) {
    width: 100%;
  }
  @media (min-width: $albumWidth * 2 + 1) and (max-width: $albumWidth * 3) {
    width: math.div(100%, 2); // 50%
  }
  @media (min-width: $albumWidth * 3 + 1) and (max-width: $albumWidth * 4) {
    width: math.div(100%, 3); // 33%
  }
  @media (min-width: $albumWidth * 4 + 1) and (max-width: $albumWidth * 6) {
    width: math.div(100%, 4); // 25%
  }
  @media (min-width: $albumWidth * 6 + 1) {
    width: math.div(100%, 6); // 16.67%
  }

  @include fade();
}
</style>
