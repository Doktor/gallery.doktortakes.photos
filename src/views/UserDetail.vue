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

    <section>
      <h2 style="text-align: left;">Albums</h2>
      <SearchAlbums />
    </section>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import FixedWidthContainer from "@/components/FixedWidthContainer";
  import SearchAlbums from "@/components/albumList/SearchAlbums";


  export default {
    components: {
      SearchAlbums,
      FixedWidthContainer,
    },

    computed: {
      ...mapState([
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
  }
</script>
