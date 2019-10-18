<template>
  <div v-if="!loading">
    <section id="photo">
      <a class="photo-link" ref="viewer">
        <img
            class="photo-landscape"
            :class="{'hidden': isPortrait}"
            :src="photo.image"
            alt="Container for landscape photos"
            title="Click to zoom"
            ref="image"
        >
        <img
            class="photo-portrait"
            :class="{'hidden': isLandscape}"
            :src="photo.image"
            alt="Container for portrait photos"
            title="Click to zoom"
            ref="image"
        >
      </a>
    </section>

    <Filmstrip
        :photos="photos"
        :position="photo.index"
    />

    <section class="info">
      <Metadata :photo="photo"/>
      <Exif :exif="photo.exif"/>
      <KeyboardShortcuts/>
      <Links/>
    </section>

    <PhotoSwipe/>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import {router} from "../router/main.js";

  import Exif from "../components/photo/Exif.vue";
  import Filmstrip from "../components/photo/Filmstrip.vue";
  import KeyboardShortcuts from '../components/photo/KeyboardShortcuts.vue';
  import Links from "../components/photo/Links.vue";
  import Metadata from "../components/photo/Metadata.vue";
  import PhotoSwipe from "../components/photo/PhotoSwipe.vue";
  import initPhotoSwipe from "../photoswipe.js";


  export default {
    components: {
      Exif,
      Filmstrip,
      KeyboardShortcuts,
      Links,
      Metadata,
      PhotoSwipe,
    },

    computed: {
      ...mapState([
        'album',
        'loading',
        'photo',
        'photos',
      ]),

      isLandscape() {
        return this.photo.width >= this.photo.height;
      },

      isPortrait() {
        return !this.isLandscape;
      },

      md5() {
        return this.$route.params.md5;
      },

      routePath() {
        return this.$route.params.routePath;
      },
    },

    created() {
      this.$store.dispatch('getAlbum', {
        routePath: this.routePath,
        setDocumentTitle: 'updateDocumentTitle',
        md5: this.md5,
      });
    },

    destroyed() {
      this.toggleClasses(false);
    },

    methods: {
      toggleClasses(state) {
        document.body.classList.toggle('photo-viewer', state);
        document.querySelector('.nav').classList.toggle('hidden', state);
      },

      previous() {
        this.$store.commit('setPhoto', this.photo.index - 1);
      },
      next() {
        this.$store.commit('setPhoto', this.photo.index + 1);
      },

      first() {
        this.$store.commit('setPhoto', 0);
      },
      last() {
        this.$store.commit('setPhoto', this.photos.length - 1);
      },
    },

    mounted() {
      this.toggleClasses(true);

      document.addEventListener('keyup', (event) => {
        if (event.ctrlKey || event.metaKey) {
          return;
        }

        if (event.key.startsWith("Arrow")) {
          event.preventDefault();

          switch (event.key) {
            case "ArrowLeft":
              return this.previous();
            case "ArrowRight":
              return this.next();
            case "ArrowUp":
              return this.first();
            case "ArrowDown":
              return this.last();
          }
        }

        switch (event.key.toLowerCase()) {
          case "a":
            return router.push({name: "album", params: {path: this.album.path}});
          case "l":
            return router.push({name: "albums"});
          case "d":
            window.location.href = this.photo.download;
            break;
          case "h":
            window.location.href = "/";
            break;
        }
      });

      let unsubscribe = this.$store.subscribe((mutation, state) => {
        if (mutation.type !== 'setLoading' || mutation.payload !== false) {
          return;
        }

        this.$nextTick(() => initPhotoSwipe.bind(this)());
        unsubscribe();
      });
    },
  }
</script>

<style>
  body.photo-viewer {
    margin: 0;
    width: 100%;
    max-width: none;
  }
</style>

<style lang="scss" scoped>
  #photo {
    display: flex;
    justify-content: center;
    align-items: center;

    margin: 0;
    width: 100%;

    @media (min-width: 1201px) {
      height: 100vh;
    }

    img {
      max-width: 100%;
      max-height: 100vh;
    }
  }

  .info, footer {
    margin: 0 auto;
    width: 90%;
  }

  .info {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    flex-wrap: wrap;

    text-align: left;
    margin-top: 2rem;

    max-width: 1000px;
  }

  .info > div {
    width: 100%;
    margin-bottom: 1rem;

    @media (min-width: 901px) {
      width: 50%;
    }
  }

  .info::v-deep {
    dl, dt, dd {
      margin: 0;
    }

    dt, dd {
      display: inline;
    }
  }

</style>
