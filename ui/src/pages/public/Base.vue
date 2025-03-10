<template>
  <div id="app">
    <div>
      <Navlinks />

      <footer>
        <div v-if="tagline" class="tagline">
          "<span v-html="tagline"></span>"
        </div>

        <p>
          website and photos
          <router-link :to="{ name: 'copyright' }">&copy;</router-link> Doktor
        </p>
      </footer>
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
import { TaglineService } from "@/services/TaglineService";

export default {
  components: {
    FadeTransition,
    Navlinks,
    Notifications,
  },

  data() {
    return {
      tagline: "",
    };
  },

  async created() {
    this.tagline = await TaglineService.getTagline();
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

.tagline {
  @include variables.headings-font();
  color: variables.$text-color;
  font-size: 1.6rem;
  font-weight: 400;

  margin: 1rem 0;
  width: 100%;
}
</style>
