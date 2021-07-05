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
      <div v-if="tagline" class="tagline">"<span v-html="tagline"/>"</div>

      <p>photos are free for personal use<br/>website and photos <router-link :to="{name: 'copyright'}">&copy;</router-link> Doktor</p>
    </footer>
  </div>
</template>

<script>
  import Navlinks from "@/components/navlink/Navlinks";
  import Notifications from "@/components/Notifications";
  import {tagline} from "@/store";


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
  margin-top: 3rem;
}
</style>