<template>
  <div id="app" :class="{ 'app-single-column': !showNavigation }">
    <Sidebar v-if="showNavigation" />

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
import { mapState } from "vuex";

export default {
  components: {
    FadeTransition,
    Sidebar,
    Notifications,
  },

  computed: {
    ...mapState(["showNavigation"]),
  },
};
</script>

<style lang="scss">
#app {
  display: block;

  @media (width > (variables.$sidebar-width + variables.$album-width)) {
    display: grid;
    grid-template-columns: variables.$sidebar-width 1fr;
    gap: variables.$sidebar-margin;
  }
}

.app-single-column {
  display: block !important;
}
</style>
