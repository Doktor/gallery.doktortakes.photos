<template>
  <div id="app">
    <Navlinks
      v-if="!isIndex"
      :showDividers="true"
      :showLogo="true"
    />

    <Notifications/>

    <FadeTransition :duration="200" mode="out-in">
      <router-view id="content" />
    </FadeTransition>

    <footer v-if="!isIndex">
      <div v-if="tagline" class="tagline">"<span v-html="tagline"/>"</div>

      <p>photos are free for personal use<br/>website and photos <router-link :to="{name: 'copyright'}">&copy;</router-link> Doktor</p>
    </footer>
  </div>
</template>

<script>
  import Navlinks from "@/components/navlink/Navlinks";
  import Notifications from "@/components/Notifications";
  import {tagline} from "@/store";
  import FadeTransition from "@/transitions/FadeTransition";


  export default {
    components: {
      FadeTransition,
      Navlinks,
      Notifications,
    },

    computed: {
      isIndex() {
        return this.$route.name === 'index';
      },

      tagline() {
        return tagline;
      },
    },
  }
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
