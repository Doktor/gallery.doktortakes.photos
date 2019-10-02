<template>
  <div v-if="!loading">
    <div>
      <h2>Views</h2>
      <p>View the list of albums in different formats.</p>
      <ul>
        <li>
          <router-link
              title="Cards"
              :to="{name: 'albums'}"
          >
            Cards
          </router-link> &mdash; default
        </li>
        <li>
          <router-link
              title="Detailed cards"
              :to="{name: 'albums', query: {view: 'detailed'}}"
          >
            Detailed cards
          </router-link> &mdash; locations, dates, other metadata
        </li>
        <li>
          <router-link
              title="Cards"
              :to="{name: 'albums', query: {view: 'simple'}}"
          >
            Simple
          </router-link> &mdash; text only
        </li>
      </ul>
    </div>

    <div>
      <h2>Special pages</h2>
      <ul>
        <!-- TODO: Add user albums link -->
        <li><a title="User albums" href="">View your albums</a></li>
        <li><a title="Tags" href="/tags/">View all tags</a></li>
        <li><a title="Search" href="search/">Search all photos</a></li>
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

      <template v-if="results.length">
        <Albums v-if="view === undefined || view === 'default'"
                :albums="results"/>

        <section v-else-if="view === 'detailed'" class="album-list-dc">
          <AlbumListDetailedCards :albums="results"/>
        </section>

        <section v-else-if="view === 'simple'">
          <AlbumListSimple :albums="results"/>
        </section>
      </template>
      <div v-else>No albums found.</div>
    </div>
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
      }
    },

    created() {
      this.$store.dispatch('getAlbums');
      document.body.classList.add('small');
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
