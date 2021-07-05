<template>
  <div>
    <template v-if="!loading">
      <h2>
        <router-link :to="{name: 'newAlbum'}">Add new album</router-link>
      </h2>

      <h2>Edit existing album</h2>

      <AlbumSearchInput v-model="search" @input="filterAlbums" />

      <div class="count">
        {{ results.length }} album{{ results.length|pluralize}}
      </div>

      <Albums v-if="results.length" :albums="results" :albumRoute="'editAlbum'"/>
      <div v-else>No albums found.</div>
    </template>
  </div>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "@/components/albumList/Albums";
  import AlbumListSimple from "@/components/albumList/AlbumListSimple";
  import AlbumSearchInput from "@/components/albumList/AlbumSearchInput.vue";


  export default {
    components: {
      AlbumSearchInput,
      Albums,
      AlbumListSimple,
    },

    computed: {
      ...mapFields([
        'search',
      ]),
      ...mapState([
        'albums',
        'results',
        'loading',
      ]),

      view() {
        return this.$route.query.view;
      },
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

    methods: {
      ...mapMutations([
        'filterAlbums',
      ]),
    },
  }
</script>
