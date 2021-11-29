<template>
  <transition
    name="fast-fade"
    mode="out-in"
    enter-class="fade-enter"
    enter-to-class="fade-enter-to"
    leave-class="fade-leave"
    leave-to-class="fade-leave-to"
  >
    <div v-if="loading" key="loading" class="index-loading-container">
      <h2 class="loading-text">Loading</h2>
      <span class="loading-text loading-1">.</span>
      <span class="loading-text loading-2">.</span>
      <span class="loading-text loading-3">.</span>
    </div>
    <div v-else key="done-loading" class="index-main-container" @click="loadNextHeroPhoto">
      <transition
        name="slow-fade"
        mode="in-out"
        enter-class="fade-enter"
        enter-to-class="fade-enter-to"
        leave-class="fade-leave"
        leave-to-class="fade-leave-to"
      >
        <div
          class="hero-photo"
          :key="heroPhoto.image"
          :style="heroPhotoStyles"
        >
          <img
            class="hero-photo-loader"
            :src="heroPhoto.image"
            @load.once="onInitialImageLoad"
            alt=""
          />
        </div>
      </transition>

      <header class="index-container index-header">
        <IndexLogo />
        <IndexNavlinks />
      </header>
    </div>
  </transition>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumListCards from "@/components/albumList/AlbumListCards";
  import IndexNavlinks from "@/components/navlink/IndexNavlinks";
  import IndexLogo from "@/components/index/IndexLogo";

  function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
 }

  export default {
    components: {
      IndexLogo,
      IndexNavlinks,
      AlbumListCards,
    },

    data() {
      return {
        heroPhotos: [],
        heroPhoto: undefined,
        index: 0,
        initialImageLoaded: false,
      }
    },

    computed: {
      ...mapState([
        'albums',
        'loading',
      ]),

      heroPhotoStyles() {
        let styles = {
          backgroundImage: `url(${this.heroPhoto.image})`,
          backgroundPositionX: this.heroPhoto.x_position ?? 'center',
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
      loadNextHeroPhoto() {
        this.heroPhoto = this.heroPhotos[this.index];
        this.index = (this.index + 1) % this.heroPhotos.length;
      },
    },

    async created() {
      this.$store.commit('setLoading', true);
      this.heroPhotos = await this.$store.dispatch('getHeroPhotos');
      shuffle(this.heroPhotos);

      this.loadNextHeroPhoto();

      await this.$store.dispatch('getAllAlbums');
      this.$store.commit('setAlbumsToTopLevelAlbums');
      this.$store.commit('setAlbumPage', 1);
      this.$store.commit('setLoading', false);
    },
  }
</script>

<style scoped lang="scss">
$panel-padding: 1.2rem;
$panel-margin: 2rem;

.index-loading-container {
  display: flex;
  justify-content: center;
  align-items: center;

  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;

  width: 100%;
  height: 100%;
}

.loading-text {
  color: $text-color-2;
  font-size: 50px;
}

.loading-1, .loading-2, .loading-3 {
  font-weight: 700;

  opacity: 0;
  animation: dot 1200ms infinite;
}

.loading-1 {
  animation-delay: 0ms;
}
.loading-2 {
  animation-delay: 200ms;
}
.loading-3 {
  animation-delay: 400ms;
}

@keyframes dot {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
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

  @media (min-width: 901px) {
    padding: $panel-padding * 1.25;
    text-align: left;
  }
}

.hero-photo {
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
  transition: opacity 1.0s ease-in-out;

  cursor: pointer;
}
.hero-photo-loader {
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

.fast-fade-enter-active,
.fast-fade-leave-active {
  transition: opacity 0.2s ease-in-out;
}

.slow-fade-enter-active,
.slow-fade-leave-active {
  transition: opacity 1.0s ease-in-out;
}
</style>
