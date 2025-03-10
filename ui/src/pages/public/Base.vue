<template>
  <div id="app">
    <div>
      <Navlinks />
    </div>

    <FadeTransition appear :duration="200" mode="out-in">
      <router-view id="content" />
    </FadeTransition>

    <Notifications />
  </div>
</template>

<script>
import Navlinks from "@/components/navlink/Navlinks";
import Notifications from "@/components/Notifications";
import FadeTransition from "@/transitions/FadeTransition";

export default {
  components: {
    FadeTransition,
    Navlinks,
    Notifications,
  },
};
</script>

<style lang="scss">
#app {
  display: block;

  @media (width > (variables.$sidebar-width + variables.$album-width)) {
    display: grid;
    grid-template-columns: variables.$sidebar-width 1fr;
    gap: variables.$page-margin;
  }
}

#content {
  flex: 1;
}
</style>
