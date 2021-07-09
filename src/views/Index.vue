<template>
  <div v-if="!loading" @click="loadNextCoverPhoto">
    <transition name="fade" mode="in-out">
      <div
        class="cover-photo"
        :key="coverPhoto.link"
        :style="coverPhotoStyles"
      >
        <img
          class="cover-photo-loader"
          :src="coverPhoto.link"
          @load.once="onInitialImageLoad"
          alt=""
        />
      </div>
    </transition>

    <header class="index-container index-header">
      <h1 class="logo">Doktor Takes Photos</h1>

      <IndexNavlinks />
    </header>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumListCards from "@/components/albumList/AlbumListCards";
  import {coverPhotos} from "@/data/cover_photos.json";
  import IndexNavlinks from "@/components/navlink/IndexNavlinks";

  function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
 }

  export default {
    components: {
      IndexNavlinks,
      AlbumListCards,
    },

    data() {
      return {
        coverPhotos: [],
        coverPhoto: undefined,
        index: 0,
        initialImageLoaded: false,
      }
    },

    computed: {
      ...mapState([
        'albums',
        'loading',
      ]),

      coverPhotoStyles() {
        let styles = {
          backgroundImage: `url(${this.coverPhoto.link})`,
        };

        if (!this.initialImageLoaded) {
          styles.visibility = 'hidden';
          styles.opacity = 0;
        }

        return styles;
      },
    },

    methods: {
      onInitialImageLoad() {
        this.initialImageLoaded = true;
      },
      loadNextCoverPhoto() {
        this.coverPhoto = this.coverPhotos[this.index];
        this.index = (this.index + 1) % this.coverPhotos.length;
      }
    },

    async created() {
      this.coverPhotos = coverPhotos.filter(photo => photo.include !== false);
      shuffle(this.coverPhotos);

      this.loadNextCoverPhoto();

      await this.$store.dispatch('getAllAlbums');
      this.$store.commit('setAlbumsToTopLevelAlbums');
      this.$store.commit('setAlbumPage', 1);
    },
  }
</script>

<style scoped lang="scss">
$panel-padding: 1.2rem;
$panel-margin: 2rem;
$logo-size: 3.2rem;

$break: 901px;

.logo {
  @include logo-font();

  font-size: $logo-size;
  line-height: 1;
  text-align: center;
  text-transform: capitalize;

  padding: 0;
  margin: 0;
  margin-bottom: 1.2rem;

  @media (min-width: $break) {
    font-size: $logo-size * 1.2;
    text-align: left;
  }
}

.index-container {
  left: 0;
  top: 0;
  position: fixed;

  margin: $panel-margin;
  padding: $panel-padding;

  background-color: rgba(black, 0.5);
  color: white;
  text-align: center;
  user-select: none;

  @media (min-width: $break) {
    padding: $panel-padding * 1.25;
    text-align: left;
  }
}

.cover-photo {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: -1;

  transform: scale(1.2);

  background-repeat: no-repeat;
  background-position: center center;
  background-attachment: fixed;
  background-size: cover;

  opacity: 1;
  transition: opacity 1.2s ease-in-out;

  cursor: pointer;
}
.cover-photo-loader {
  display: none;
}

.fade-enter {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}

.fade-leave {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1.2s ease-in-out;
}
</style>
