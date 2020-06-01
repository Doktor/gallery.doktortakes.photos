<template>
  <div>
    <template v-if="!loading">
      <h2>
        <router-link :to="{name: 'newAlbum'}">Add new album</router-link>
      </h2>

      <h2>Edit existing album</h2>

      <div class="album-search-container">
        <input
            type="text"
            placeholder="Search by name..."
            v-model="search"
            @keyup="filterAlbums"
        >
      </div>

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
  import Albums from "../components/albumList/Albums.vue";
  import AlbumListDetailedCards from "../components/albumList/AlbumListDetailedCards.vue";
  import AlbumListSimple from "../components/albumList/AlbumListSimple.vue";


  export default {
    components: {
      Albums,
      AlbumListDetailedCards,
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
