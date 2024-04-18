<template>
  <main v-if="!loading">
    <div class="sidebar">
      <h2>Photos</h2>
      <ul>
        <li @click="selectRecentPhotos">
          <a href="#">Recent photos</a>
        </li>
      </ul>

      <h2>Albums</h2>
      <ul>
        <li v-for="album in albums" :key="album.id" @click="selectAlbum(album)">
          <a href="#">{{ album.name }}</a>
        </li>
      </ul>
    </div>

    <div v-if="showRecentPhotos">
      <h2 style="text-align: left">Recent photos</h2>
      <PhotoGallery
        routeName="editPhoto"
        :useServerSidePagination="true"
        :getPage="getRecentPhotosPage"
      />
    </div>
    <div v-else-if="selectedAlbum !== null" class="contents">
      <section class="album-cover-container">
        <AlbumCover :album="selectedAlbum" :count="photos.length" />
      </section>

      <PhotoGallery :photos="photos" />
    </div>
  </main>
</template>

<script>
import { AlbumService } from "@/services/AlbumService";
import PhotoGallery from "@/components/photoList/PhotoGallery.vue";
import AlbumCover from "@/pages/public/AlbumDetailPage/AlbumCover.vue";
import { ManagePhotoService } from "@/services/manage/ManagePhotoService";

export default {
  components: { AlbumCover, PhotoGallery },
  data() {
    return {
      loading: true,
      albums: [],

      showRecentPhotos: true,
      selectedAlbum: null,
      photos: [],
    };
  },

  async created() {
    this.loading = true;
    this.albums = await AlbumService.getAllAlbums();
    this.loading = false;
  },

  methods: {
    selectAlbum(album) {
      this.showRecentPhotos = false;
      this.selectedAlbum = album;
    },

    selectRecentPhotos() {
      this.showRecentPhotos = true;
    },
    async getRecentPhotosPage(page, size) {
      let { ok, content } = await ManagePhotoService.getRecentPhotos(
        page,
        size,
      );

      if (!ok) {
        this.$store.commit("addNotification", {
          message: "An error occurred when retrieving recent photos",
          status: "error",
        });

        return { photos: [], count: 0 };
      } else {
        return content;
      }
    },
  },

  watch: {
    async selectedAlbum(newAlbum, oldAlbum) {
      if (newAlbum === oldAlbum) {
        return;
      }

      let { ok, photos } = await AlbumService.getAlbumPhotos({
        path: newAlbum.path,
      });

      if (!ok) {
        console.error("an error occurred when fetching photos for this album");
        this.photos = [];

        return;
      }

      this.photos = photos;
    },
  },
};
</script>

<style lang="scss" scoped>
main {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}

$sidebar-width: 20%;

.sidebar {
  width: $sidebar-width;
  border: 1px solid lightgray;
  margin-right: 2rem;

  ul {
    list-style-type: none;

    margin: 0;
    padding: 0;

    text-align: left;
  }
}

.contents {
  width: 100% - $sidebar-width;
}
</style>
