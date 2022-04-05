<template>
  <div id="app">
    <Navlinks v-if="!isIndex" :showDividers="true" :showLogo="true" />

    <Notifications />

    <FadeTransition appear :duration="200" mode="out-in">
      <router-view id="content" />
    </FadeTransition>

    <footer v-if="!isIndex">
      <div v-if="tagline" class="tagline">"<span v-html="tagline" />"</div>

      <p>
        photos are free for personal use<br />website and photos
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

  computed: {
    isIndex() {
      return this.$route.name === "index";
    },
  },

  async created() {
    this.tagline = await TaglineService.getTagline();
  },
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  min-height: 100vh;
}

#content {
  flex: 1;
}
</style>
