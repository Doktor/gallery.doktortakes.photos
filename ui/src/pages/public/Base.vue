<template>
  <main class="app" :class="{ 'app-single-column': !showNavigation }">
    <Sidebar v-if="showNavigation" />

    <div id="content">
      <Breadcrumbs v-if="breadcrumbs.length" :items="breadcrumbs" />
      <router-view />
    </div>

    <Notifications />
  </main>
</template>

<script>
import Breadcrumbs from "@/components/Breadcrumbs";
import Sidebar from "@/components/sidebar/Sidebar";
import Notifications from "@/components/Notifications";
import FadeTransition from "@/transitions/FadeTransition";
import { mapState } from "vuex";

export default {
  components: {
    Breadcrumbs,
    FadeTransition,
    Sidebar,
    Notifications,
  },

  computed: {
    ...mapState(["showNavigation", "breadcrumbs"]),
  },
};
</script>

<style lang="scss">
.app {
  display: grid;
  grid-template-columns: 1fr;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    grid-template-columns: variables.$sidebar-width 1fr;
    gap: variables.$sidebar-margin;
  }
}

.app-single-column {
  display: block !important;
}
</style>
