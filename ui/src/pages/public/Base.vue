<template>
  <div id="app">
    <div>
      <Sidebar />
    </div>

    <FadeTransition appear :duration="200" mode="out-in">
      <router-view id="content" />
    </FadeTransition>

    <Notifications />
  </div>
</template>

<script>
import Sidebar from "@/components/navlink/Sidebar";
import Notifications from "@/components/Notifications";
import FadeTransition from "@/transitions/FadeTransition";

export default {
  components: {
    FadeTransition,
    Sidebar,
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
