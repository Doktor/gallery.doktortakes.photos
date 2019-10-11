<template>
  <div>
    <template v-if="!loading">
      <h2>
        <router-link :to="{name: 'newAlbum'}">Add new album</router-link>
      </h2>

      <h2>Edit existing album</h2>

      <ul>
        <li>
          <router-link
              title="Cards"
              :to="{name: 'index'}"
          >
            Cards
          </router-link>
        </li>
        <li>
          <router-link
              title="Detailed cards"
              :to="{name: 'index', query: {view: 'detailed'}}"
          >
            Detailed cards
          </router-link>
        </li>
        <li>
          <router-link
              title="Cards"
              :to="{name: 'index', query: {view: 'simple'}}"
          >
            Simple
          </router-link>
        </li>
      </ul>

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

      <Albums v-if="results.length" :albums="results" :route="'editAlbum'"/>
      <div v-else>No albums found.</div>
    </template>
  </div>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "../components/Albums.vue";
  import AlbumListDetailedCards from "../components/AlbumListDetailedCards.vue";
  import AlbumListSimple from "../components/AlbumListSimple.vue";


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
      this.$store.dispatch('getAlbums');
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
