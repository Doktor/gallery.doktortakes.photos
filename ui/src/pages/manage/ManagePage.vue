<template>
  <div v-if="!loading">
    <FixedWidthContainer>
      <h2>Edit</h2>

      <ul>
        <li>
          <router-link :to="{ name: 'newAlbum' }">Add new album</router-link>
        </li>
        <li><router-link :to="{ name: 'groups' }">View groups</router-link></li>
        <li><router-link :to="{ name: 'users' }">View users</router-link></li>
      </ul>
    </FixedWidthContainer>

    <h3 style="text-align: left">Recently uploaded photos</h3>
    <PhotoGallery :photos="recentPhotos" routeName="editPhoto" />

    <AlbumGallery :albums="albums" :loading="loading" albumRoute="editAlbum" />
  </div>
</template>

<script>
import AlbumGallery from "../../components/albumList/AlbumGallery.vue";
import FixedWidthContainer from "../../components/FixedWidthContainer.vue";
import { AlbumService } from "../../services/AlbumService";
import PhotoGallery from "../../components/photoList/PhotoGallery.vue";
import { ManagePhotoService } from "../../services/manage/ManagePhotoService";

export default {
  components: {
    PhotoGallery,
    FixedWidthContainer,
    AlbumGallery,
  },

  data() {
    return {
      albums: [],
      recentPhotos: [],
      loading: true,
    };
  },

  async created() {
    this.loading = true;
    this.albums = await AlbumService.getAllAlbums();

    let { ok, content } = await ManagePhotoService.getRecentPhotos(12);

    if (!ok) {
      this.recentPhotos = [];
      this.$store.commit("addNotification", {
        message: "An error occurred when retrieving recent photos",
        status: "error",
      });
    } else {
      this.recentPhotos = content;
    }

    this.loading = false;
  },
};
</script>
