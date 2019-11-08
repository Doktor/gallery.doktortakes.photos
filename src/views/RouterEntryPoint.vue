<template>
  <div id="app">
    <header v-if="isIndex">
      <h1 class="logo logo-large">Doktor Takes Photos</h1>
      <Navlinks
          class="nav-items nav-items-index"
          :showDividers="false"
          :showLogo="false"
      />
    </header>
    <nav v-else class="nav">
      <Navlinks
          class="nav-items"
          :showDividers="true"
          :showLogo="true"
      />
    </nav>

    <div id="messages"></div>

    <router-view/>

    <footer>
      <div v-if="tagline" class="tagline">"{{ tagline }}"</div>

      <p>Photos are free for personal use <router-link :to="{name: 'copyright'}">(Details)</router-link></p>
      <p class="copyright">Website and photos <router-link :to="{name: 'copyright'}">&copy;</router-link> Doktor 2016&ndash;2019</p>
    </footer>
  </div>
</template>

<script>
  import Navlinks from "../components/Navlinks.vue";
  import {tagline} from "../store";


  export default {
    components: {
      Navlinks,
    },

    computed: {
      isIndex() {
        return this.route === 'index';
      },

      tagline() {
        return tagline;
      },

      route() {
        return this.$route.name;
      },
    },
  }
</script>
