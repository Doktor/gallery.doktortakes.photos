<template>
  <div v-if="!loading">
    <h2>
      <router-link :to="{name: 'newAlbum'}">Add new album</router-link>
    </h2>

    <div class="count">
      {{ results.length }} album{{ results.length|pluralize}}
    </div>

    <SearchAlbums />
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import SearchAlbums from "@/components/albumList/SearchAlbums";


  export default {
    components: {
      SearchAlbums,
    },

    computed: {
      ...mapState([
        'albums',
        'results',
        'loading',
      ]),
    },

    created() {
      this.$store.dispatch('getAllAlbums').then(() => {
        this.$store.commit('setAlbumsToTopLevelAlbums');
        this.$store.commit('setAlbumPage', 1);
      })
    },

    filters: {
      pluralize(value) {
        return value === 1 ? '' : 's';
      },
    },
  }
</script>
