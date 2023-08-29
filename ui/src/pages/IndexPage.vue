<template>
  <FadeTransition appear :duration="500" mode="out-in">
    <div v-if="loading" key="loading" class="index-loading-container">
      <h2 class="loading-text">Loading</h2>
      <span class="loading-text loading-1">.</span>
      <span class="loading-text loading-2">.</span>
      <span class="loading-text loading-3">.</span>
    </div>
    <div
      v-else
      key="done-loading"
      class="index-main-container"
      @click="loadNextHeroPhoto"
    >
      <HeroPhoto :photo="heroPhoto" />

      <header class="index-container index-header">
        <IndexLogo />
        <IndexNavlinks />
      </header>
    </div>
  </FadeTransition>
</template>

<script>
import { mapState } from "vuex";
import AlbumListTiles from "../components/albumList/AlbumListTiles.vue";
import IndexNavlinks from "../components/navlink/IndexNavlinks.vue";
import IndexLogo from "../components/index/IndexLogo.vue";
import FadeTransition from "../transitions/FadeTransition.vue";
import HeroPhoto from "../components/index/HeroPhoto.vue";
import { HeroPhotoService } from "../services/HeroPhotoService";

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

export default {
  components: {
    HeroPhoto,
    FadeTransition,
    IndexLogo,
    IndexNavlinks,
    AlbumListTiles,
  },

  data() {
    return {
      heroPhotos: [],
      heroPhoto: undefined,
      heroPhotoIndex: 0,
    };
  },

  computed: {
    ...mapState(["albums", "loading"]),
  },

  methods: {
    loadNextHeroPhoto() {
      this.heroPhoto = this.heroPhotos[this.heroPhotoIndex];
      this.heroPhotoIndex = (this.heroPhotoIndex + 1) % this.heroPhotos.length;
    },
  },

  async created() {
    this.$store.commit("setLoading", true);

    this.heroPhotos = await HeroPhotoService.list();
    shuffle(this.heroPhotos);
    this.loadNextHeroPhoto();

    this.$store.commit("setLoading", false);
  },
};
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

.loading-1,
.loading-2,
.loading-3 {
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
</style>
