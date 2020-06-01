<template>
  <div v-if="!loading">
    <div>
      <h2>{{ user.name }}</h2>

      <ul>
        <li>Account created: {{ user.account_created }}</li>
        <li>Last sign in: {{ user.last_sign_in }}</li>
      </ul>
    </div>

    <div>
      <h2>User settings</h2>

      <ul>
        <li>
          <router-link :to="{name: 'changePassword', params: {slug: user.name}}">
            Change your password
          </router-link>
        </li>
      </ul>
    </div>

    <div>
      <h2>Albums</h2>

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

      <Albums v-if="results.length" :albums="results" :albumRoute="'album'"/>
      <div v-else>No albums found.</div>
    </div>
  </div>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "../components/albumList/Albums.vue";


  export default {
    components: {
      Albums,
    },

    computed: {
      ...mapFields([
        'search',
      ]),
      ...mapState([
        'results',
        'loading',
        'user',
      ]),
    },

    created() {
      this.$store.dispatch('getAllAlbums').then(() => {
        this.$store.commit('setAlbumsToPrivateAlbums');
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
