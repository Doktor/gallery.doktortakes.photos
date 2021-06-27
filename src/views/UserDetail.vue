<template>
  <div v-if="!loading">
    <FixedWidthContainer>
      <h2>{{ user.name }}</h2>

      <ul>
        <li>Account created: {{ user.account_created }}</li>
        <li>Last sign in: {{ user.last_sign_in }}</li>
      </ul>
    </FixedWidthContainer>

    <FixedWidthContainer>
      <h2>User settings</h2>

      <ul>
        <li>
          <router-link :to="{name: 'changePassword', params: {slug: user.name}}">
            Change your password
          </router-link>
        </li>
      </ul>
    </FixedWidthContainer>

    <FixedWidthContainer>
      <h2>Albums</h2>

      <div class="album-search-container">
        <input
            type="text"
            placeholder="Search by name..."
            v-model="search"
            @keyup="filterAlbums"
        >
      </div>
    </FixedWidthContainer>

    <div>
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
  import Albums from "@/components/albumList/Albums";
  import FixedWidthContainer from "@/components/FixedWidthContainer";


  export default {
    components: {
      Albums,
      FixedWidthContainer,
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
