<template>
  <div v-if="!loading && Object.keys(photo).length !== 0">
    <PhotoViewer
        :count="this.photos.length - 1"
        :onClick="onClick"
        :photo="photo"
    />

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
  import PhotoViewer from "../components/PhotoViewer.vue";
  import initPhotoSwipe from "../photoswipe.js";


  export default {
    beforeRouteEnter(to, from, next) {
      next(view => document.addEventListener('keyup', view.handleKey));
    },

    beforeRouteLeave(to, from, next) {
      document.removeEventListener('keyup', this.handleKey);
      next();
    },

    components: {
      PhotoViewer,
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

      md5() {
        return this.$route.params.md5;
      },

      routeAccessCode() {
        return this.$route.query.code || "";
      },

      routePath() {
        return this.$route.params.path;
      },
    },

    created() {
      this.$store.dispatch('getAlbum', {rawPath: this.routePath, code: this.routeAccessCode}).then(() => {
        this.$store.commit('setPhotoInitial', {md5: this.md5, code: this.routeAccessCode});
      });
    },

    data() {
      return {
        onClick: () => {},
      }
    },

    methods: {
      handleKey(event) {
        if (event.ctrlKey || event.metaKey) {
          return;
        }

        switch (event.key.toLowerCase()) {
          case "a":
            return router.push({name: "album", params: {path: this.album.pathSplit}});
          case "l":
            return router.push({name: "albums"});
          case "d":
            window.location.href = this.photo.download;
            break;
          case "h":
            window.location.href = "/";
            break;
        }
      },
    },

    mounted() {
      let unsubscribe = this.$store.subscribe((mutation, state) => {
        if (mutation.type !== 'setPhoto') {
          return;
        }

        this.$nextTick(() => this.onClick = initPhotoSwipe.bind(this)());
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
