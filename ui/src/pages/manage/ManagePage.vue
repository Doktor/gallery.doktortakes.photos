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
    <PhotoGallery
      routeName="editPhoto"
      :useServerSidePagination="true"
      :getPage="getPage"
    />

    <AlbumGallery :albums="albums" :loading="loading" albumRoute="editAlbum" />
  </div>
</template>

<script>
import AlbumGallery from "@/components/albumList/AlbumGallery";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import { AlbumService } from "@/services/AlbumService";
import PhotoGallery from "@/components/photoList/PhotoGallery";
import { ManagePhotoService } from "@/services/manage/ManagePhotoService";

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

  methods: {
    async getPage(page, size) {
      let { ok, content } = await ManagePhotoService.getRecentPhotos(
        page,
        size
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

  async created() {
    this.loading = true;
    this.albums = await AlbumService.getAllAlbums();
    this.loading = false;
  },
};
</script>
