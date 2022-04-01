<template>
  <div v-if="!loading && Object.keys(photo).length !== 0">
    <PhotoViewer
        :count="this.photos.length - 1"
        :onClick="onClick"
        :photo="photo"
        @changePhoto="changePhoto"
    />

    <Filmstrip
        :photos="photos"
        :position="photo.index"
        @changePhoto="changePhoto"
    />

    <section class="info">
      <Metadata :photo="photo" :count="photos.length" />
      <Exif :exif="photo.exif" />
      <KeyboardShortcuts />
      <Links :album="album" />
    </section>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import {router} from "@/router/main.js";

import Exif from "@/components/photoDetail/Exif";
import Filmstrip from "@/components/photoDetail/Filmstrip";
import KeyboardShortcuts from '@/components/photoDetail/KeyboardShortcuts.vue';
import Links from "@/components/photoDetail/Links";
import Metadata from "@/components/photoDetail/Metadata";
import PhotoViewer from "@/components/photoDetail/PhotoViewer";
import {AlbumService} from "@/services/AlbumService";

const photoTitleTemplate = "{0} | {1} | Doktor Takes Photos";


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
  },

  data() {
    return {
      album: {},
      photos: [],

      onClick: () => {
      },
      photo: {},
    }
  },

  computed: {
    ...mapState([
      'loading',
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

  async created() {
    let {ok, album, photos} = await AlbumService.getAlbum({rawPath: this.routePath, code: this.routeAccessCode});

    if (!ok) {
      this.$store.commit('addNotification', "Album not found.");
      await this.$router.push({name: 'albums'});

      return;
    }

    this.album = album;
    this.photos = photos;

    let photo = this.photos.find(photo => photo.md5 === this.md5);
    this.setPhoto(photo, this.routeAccessCode);
  },

  methods: {
    changePhoto(index) {
      if (index === this.photo.index) {
        return;
      }

      // Wrap around
      if (index < 0) {
        index = this.photos.length - 1;
      } else if (index > this.photos.length - 1) {
        index = 0;
      }

      this.setPhoto(this.photos[index]);
    },

    preloadPhoto(photo) {
      if (!photo.loaded) {
        let image = new Image();
        image.src = photo.images.display.url;

        photo.loaded = true;
      }
    },

    setPhoto(photo, code) {
      this.photo = photo;
      this.photo.loaded = true;

      // Preload previous 2 and next 2 photos
      let length = this.photos.length;
      let prev = (photo.index - 2 + length) % length;

      for (let i = prev; i < prev + 5; i++) {
        let photo = this.photos[i % length];
        this.preloadPhoto(photo);
      }

      // Add browser history entry
      let title = photoTitleTemplate.format(photo.md5.substring(0, 8), this.album.name);
      document.title = title;

      let resolved = router.resolve({
        name: 'photo',
        params: {
          path: this.album.pathSplit,
          md5: this.md5,
        },
        query: this.$route.query,
      });
      window.history.pushState(null, title, resolved.href);
    },

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
