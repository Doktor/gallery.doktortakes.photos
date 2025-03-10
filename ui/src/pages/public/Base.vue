<template>
  <div id="app">
    <Navlinks :showDividers="true" :showLogo="true" />

    <Notifications />

    <FadeTransition appear :duration="200" mode="out-in">
      <router-view id="content" />
    </FadeTransition>

    <footer>
      <div v-if="tagline" class="tagline">"<span v-html="tagline"></span>"</div>

      <p>
        website and photos
        <router-link :to="{ name: 'copyright' }">&copy;</router-link> Doktor
      </p>
    </footer>
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
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  min-height: 100vh;
}

#content {
  flex: 1;
}

.tagline {
  @include headings-font();
  color: $text-color;
  font-size: 1.6rem;
  font-weight: 400;

  margin: 1rem 0;
  width: 100%;
}
</style>
