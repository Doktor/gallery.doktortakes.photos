<template>
  <CustomButton class="sidebar-menu-button" @click="$emit('click')">
    <slot></slot>
  </CustomButton>
</template>

<script>
import CustomButton from "@/components/form/CustomButton.vue";

export default {
  components: {
    CustomButton,
  },
};
</script>

<style lang="scss">
.sidebar-menu-button {
  background: none;
  width: variables.$sidebar-width;

  border: 1px solid black;
  border-radius: 2px;
  margin: 0 auto;
  margin-bottom: variables.$sidebar-margin;
  padding: 12px;

  cursor: pointer;

  @include variables.headings-font();
  font-size: 2rem;
  text-transform: uppercase;

  &:hover {
    background-color: rgb(230, 230, 230);
  }

  &,
  &:hover {
    transition: background-color 0.1s ease-in-out;
  }
}

.open-menu-button {
  display: inline-flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: none;
  }

  .menu-icon {
    width: 1rem;
    height: 1rem;

    margin-right: 12px;
  }
}

.close-menu-button {
  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: none;
  }
}
</style>
