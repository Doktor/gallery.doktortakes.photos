<template>
  <div v-if="!loading">
    <div
      class="cover-photo"
      alt="Cover photo"
      :title="`Cover photo from ${albumTitle}`"
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
      <div>Cover photo from <router-link :to="{name: 'album', params: {path: albumSlug}}">{{ albumTitle }}</router-link></div>
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


  const coverPhotos = [
    [
      "Denver 2017",
      "cat-party",
      "https://s3.us-east-2.amazonaws.com/doktor/media/photos/20170610_035430_aedcf879.jpg"
    ],

    [
      "Midwest FurFest 2018",
      "winter-adventures",
      "https://s3.us-east-2.amazonaws.com/doktor/media/photos/20181128_155357_a05eb910.jpg",
    ],

    [
      "Top Secret Lacy Photoshoot",
      "top-secret-lacy-photoshoot",
      "https://s3.us-east-2.amazonaws.com/doktor/media/photos/20190706_224301_6ecdce63.jpg",
    ],

    [
      "New Hampshire 2019",
      "rocky-gorge",
      "https://s3.us-east-2.amazonaws.com/doktor/media/photos/20191012_180146_2d10d618.jpg",
    ],

    [
      "Anthro New England 2020",
      "garden-animals",
      "https://s3.us-east-2.amazonaws.com/doktor/media/photos/20200223_173940_8a5a5d66.jpg",
    ],
  ]

  let [title, slug, photo] = randomChoice(coverPhotos);


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

      albumSlug() {
        return slug;
      },

      albumTitle() {
        return title;
      },

      coverPhoto() {
        return photo;
      },

      coverPhotoStyles() {
        return {
          backgroundImage: `url(${this.coverPhoto})`
        }
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
$margin: 40px;

$logo-size: 3.2rem;

.logo {
  text-align: left;
  font-size: $logo-size;
  line-height: 1;
  text-transform: capitalize;

  padding: 0;
  margin: 0;
  margin-bottom: 0.7rem;

  @media (min-width: 901px) {
    font-size: $logo-size * 1.1;
  }
}

.index-header, .index-footer {
  position: fixed;
  left: $margin;

  margin: 0;
  background-color: rgba(0, 0, 0, 0.9);

  text-align: left;
  color: white;
}

.index-header {
  top: $margin;

  padding: 1.3rem;
}

.index-footer {
  bottom: $margin;

  padding: 0.8rem;

  font-size: 1.1rem;
  text-transform: unset;
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
