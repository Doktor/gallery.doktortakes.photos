<template>
  <div v-if="!loading && Object.keys(photo).length !== 0">
    <div class="photo-navigation">
      <PhotoViewer
        class="photo-viewer"
        :count="this.photos.length - 1"
        :onClick="onClick"
        :photo="photo"
        @changePhoto="changePhoto"
      />

      <Filmstrip
        class="filmstrip"
        :photos="photos"
        :position="photo.index"
        @changePhoto="changePhoto"
      />
    </div>

    <PhotoInfo :album="album" :photo="photo" :photos="photos" />
  </div>
</template>

<script>
import { mapState } from "vuex";
import { router } from "@/router";
import Filmstrip from "./Filmstrip";
import PhotoViewer from "./PhotoViewer";
import { AlbumService } from "@/services/AlbumService";
import PhotoInfo from "./PhotoInfo";

const photoTitleTemplate = "{0} | {1} | Doktor Takes Photos";

export default {
  beforeRouteEnter(to, from, next) {
    next((view) => document.addEventListener("keyup", view.handleKey));
  },

  beforeRouteLeave(to, from, next) {
    document.removeEventListener("keyup", this.handleKey);
    next();
  },

  components: {
    PhotoInfo,
    PhotoViewer,
    Filmstrip,
  },

  data() {
    return {
      album: {},
      photos: [],

      onClick: () => {},
      photo: {},
    };
  },

  computed: {
    ...mapState(["loading"]),

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
    let { ok, album, photos } = await AlbumService.getAlbum({
      rawPath: this.routePath,
      code: this.routeAccessCode,
    });

    if (!ok) {
      this.$store.commit("addNotification", {
        message: "Album not found.",
        status: "error",
      });
      await this.$router.push({ name: "albums" });

      return;
    }

    this.album = album;
    this.photos = photos;

    let photo = this.photos.find((photo) => photo.md5 === this.md5);
    this.setPhoto(photo, true);
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

    setPhoto(photo, replaceHistory = false) {
      this.photo = photo;
      this.photo.loaded = true;

      // Preload previous 2 and next 2 photos
      let length = this.photos.length;
      let prev = (photo.index - 2 + length) % length;

      for (let i = prev; i < prev + 5; i++) {
        let photo = this.photos[i % length];
        this.preloadPhoto(photo);
      }

      this.updateHistory(replaceHistory);
    },

    preloadPhoto(photo) {
      if (!photo.loaded) {
        let image = new Image();
        image.src = photo.images.display?.url ?? photo.images.original.url;

        photo.loaded = true;
      }
    },

    updateHistory(replace = false) {
      let resolved = router.resolve({
        name: "photo",
        params: {
          path: this.album.pathSplit,
          md5: this.photo.md5,
        },
        query: this.$route.query,
      });

      replace
        ? window.history.replaceState(null, null, resolved.href)
        : window.history.pushState(null, null, resolved.href);

      document.title = photoTitleTemplate.format(
        this.photo.md5.substring(0, 8),
        this.album.name,
      );
    },

    handleKey(event) {
      if (event.ctrlKey || event.metaKey) {
        return;
      }

      switch (event.key.toLowerCase()) {
        case "a":
          return router.push({
            name: "album",
            params: { path: this.album.pathSplit },
          });
        case "l":
          return router.push({ name: "albums" });
        case "h":
          window.location.href = "/";
          break;
      }
    },
  },

  watch: {
    md5(newHash) {
      let photo = this.photos.find((photo) => photo.md5 === newHash);
      this.setPhoto(photo);
    },
  },
};
</script>

<style>
body.photo-viewer {
  margin: 0;
  width: 100%;
  max-width: none;
}
</style>

<style lang="scss" scoped>
.photo-navigation {
  display: flex;
  flex-direction: column;

  width: 100%;
  height: 100vh;
}

.photo-viewer {
  flex-grow: 1;

  overflow: hidden;
  position: relative;
}

.filmstrip {
  width: 100%;

  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;

  margin: 0;
  margin-top: auto;
  padding: 1rem;
}
</style>
