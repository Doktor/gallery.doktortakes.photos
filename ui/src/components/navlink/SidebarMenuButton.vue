<template>
  <CustomButton
    class="sidebar-menu-button"
    @click="$emit('click')"
    :title="title"
  >
    <i :class="iconClass"></i>
    <span>{{ title }}</span>
  </CustomButton>
</template>

<script>
import CustomButton from "@/components/form/CustomButton";

export default {
  components: {
    CustomButton,
  },

  props: {
    iconClass: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.sidebar-menu-button {
  display: inline-flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  width: variables.$sidebar-width;

  border: 1px solid black;
  border-radius: 2px;
  margin: 0 auto;
  margin-bottom: variables.$sidebar-margin;
  padding: 12px;

  @include variables.headings-font();
  font-size: 2rem;
  text-transform: uppercase;

  cursor: pointer;
  transition: none !important;

  color: variables.$text-color;
  background-color: variables.$background-color;

  &:hover {
    color: variables.$background-color;
    background-color: variables.$text-color;
  }

  i {
    font-size: 1.6rem;
    margin-right: 12px;
  }

  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: none;
  }
}
</style>
