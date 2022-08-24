<template>
  <button class="button" type="button" v-bind="$attrs" @click="$emit('click')">
    <slot></slot>
  </button>
</template>

<style lang="scss">
@mixin button($background-color, $text-color) {
  background-color: $background-color;
  border: 1px solid darken($background-color, 8%);
  color: $text-color;

  &:focus,
  &:hover {
    background-color: darken($background-color, 8%);
  }

  &,
  &:hover {
    text-decoration: none;
    transition: background-color 0.1s;
  }
}

.button {
  display: inline-block;
  padding: 10px 14px;

  border: 0;
  border-radius: 4px;

  cursor: pointer;
  line-height: 1;
  text-align: center;

  // Default
  @include button($background-color-3, $text-color);

  &.button-primary {
    @include button($text-blue, $background-color);
  }

  &.button-danger {
    @include button(rgb(255, 30, 0), white);
  }
}
</style>
