<template>
  <div v-if="!loading">
    <div
      class="cover-photo"
      alt="Cover photo"
      :title="`Cover photo from ${coverPhoto.title}`"
      :style="coverPhotoStyles">
    </div>

    <header class="index-header">
      <h1 class="logo">Doktor Takes Photos</h1>

      <Navlinks
        class="nav-index"
        :showDividers="false"
        :showLogo="false"
      />
    </header>

    <footer class="index-footer">
      <div>
        Cover photo:
        <router-link :to="{name: 'album', params: {path: coverPhoto.slug}}">
          {{ coverPhoto.title }}
        </router-link>
      </div>
      <div>Website and photos <router-link :to="{name: 'copyright'}">&copy;</router-link> Doktor</div>
    </footer>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import {randomChoice} from '../main';
  import {router} from "../router/main";
  import {tagline} from "../store";
  import AlbumListCards from "../components/albumList/AlbumListCards.vue";
  import Navlinks from "../components/Navlinks.vue";
  import {coverPhotos} from "../data/cover_photos.json";

  const coverPhoto = randomChoice(coverPhotos);

  export default {
    components: {
      AlbumListCards,
      Navlinks,
    },

    computed: {
      ...mapState([
        'albums',
        'loading',
      ]),

      coverPhoto() {
        return coverPhoto;
      },

      coverPhotoStyles() {
        return {
          backgroundImage: `url(${coverPhoto.link})`
        };
      },
    },

    async created() {
      await this.$store.dispatch('getAllAlbums');
      this.$store.commit('setAlbumsToTopLevelAlbums');
      this.$store.commit('setAlbumPage', 1);
    },
  }
</script>

<style scoped lang="scss">
$panel-padding: 1rem;
$panel-margin: 40px;
$logo-size: 3.2rem;

.logo {
  font-size: $logo-size;
  text-align: center;
  line-height: 1.1;
  text-transform: capitalize;

  padding: 0;
  margin: 0;
  margin-bottom: 1rem;

  @media (min-width: 1201px) {
    font-size: $logo-size * 1.1;
    text-align: left;
    line-height: 1;
  }
}

.index-header, .index-footer {
  position: fixed;
  left: $panel-margin;

  margin: 0;
  background-color: rgba(0, 0, 0, 0.85);

  text-align: center;
  color: white;

  @media (min-width: 1201px) {
    text-align: left;
  }
}

.index-header {
  right: $panel-margin;
  padding: $panel-padding;

  @media (min-width: 1201px) {
    right: initial;
    padding: $panel-padding * 1.25;
  }
}

.index-footer {
  display: none;

  @media (min-width: 1201px) {
    display: block;
    padding: 0.8rem;

    bottom: $panel-margin;

    font-size: 1.1rem;
    text-transform: unset;
  }
}

.cover-photo {
  z-index: -1;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;

  transform: scale(1.2);

  background-repeat: no-repeat;
  background-position: center center;
  background-attachment: fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
}
</style>
