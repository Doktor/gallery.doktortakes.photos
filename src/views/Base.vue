<template>
  <div id="app">
    <Navlinks
      v-if="!isIndex"
      :showDividers="true"
      :showLogo="true"
    />

    <Notifications/>

    <router-view/>

    <footer v-if="!isIndex">
      <div v-if="tagline" class="tagline">"{{ tagline }}"</div>

      <p>Photos are free for personal use<br>Website and photos <router-link :to="{name: 'copyright'}">&copy;</router-link> Doktor</p>
    </footer>
  </div>
</template>

<script>
  import Navlinks from "../components/Navlinks.vue";
  import Notifications from "../components/Notifications.vue";
  import {tagline} from "../store";


  export default {
    components: {
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
footer {
  text-transform: none;
}
</style>
