<template>
  <render />
</template>

<script setup>
import { computed, h, useSlots } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  display: {
    type: String,
    default: "",
  },
  route: {
    type: String,
  },
  to: {
    type: Object,
  },
  href: {
    type: String,
  },
});

const slots = useSlots();

const toComputed = computed(() => {
  if (props.to !== undefined) {
    return props.to;
  }

  return { name: props.route };
});

const renderContent = () =>
  slots.default ? slots.default() : props.display || props.title;

const linkProps = {
  title: props.title,
  class: "sidebar-link",
};

const renderLink = () => {
  return props.route || props.to
    ? h(
        RouterLink,
        {
          ...linkProps,
          to: toComputed.value,
          exactActiveClass: "sidebar-link-active",
        },
        [renderContent()],
      )
    : h(
        "a",
        {
          ...linkProps,
          href: props.href,
          target: "blank",
          rel: "nofollow noopener noreferrer",
        },
        [renderContent()],
      );
};

const render = h("li", null, [renderLink()]);
</script>

<style lang="scss">
@mixin link($text-color, $background-color: variables.$background-color) {
  color: $text-color;
  background-color: $background-color;

  &.sidebar-link-active,
  &:hover {
    color: $background-color;
    background-color: $text-color;
  }
}

.sidebar-link {
  display: inline-block;
  padding: variables.$sidebar-link-margin;
  padding-left: variables.$sidebar-link-margin * 3;
  width: 100%;

  text-decoration-line: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 4px;

  transition: color, background-color;

  @include link(variables.$text-color);
  background-color: unset;
}

.sidebar-link {
  .sidebar-item-profile & {
    @include link(variables.$text-blue);
  }

  .sidebar-item-log-out & {
    @include link(variables.$text-error);
  }
}
</style>
