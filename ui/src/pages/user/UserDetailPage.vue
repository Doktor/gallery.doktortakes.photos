<template>
  <div v-if="!loading">
    <FixedWidthContainer>
      <h2>{{ user.name }}</h2>

      <ul>
        <li>Account created: {{ user.account_created }}</li>
        <li>Last sign in: {{ user.last_sign_in }}</li>
      </ul>
    </FixedWidthContainer>

    <FixedWidthContainer>
      <h2>User settings</h2>

      <ul>
        <li>
          <router-link
            :to="{ name: 'changePassword', params: { slug: user.name } }"
          >
            Change your password
          </router-link>
        </li>
      </ul>
    </FixedWidthContainer>

    <section>
      <h2 style="text-align: left">Albums</h2>
      <AlbumGallery :albums="albums" :loading="loading" />
    </section>
  </div>
</template>

<script>
import { mapState } from "vuex";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import AlbumGallery from "@/components/albumList/AlbumGallery";
import { AlbumService } from "@/services/AlbumService";

export default {
  components: {
    AlbumGallery,
    FixedWidthContainer,
  },

  computed: {
    ...mapState(["user"]),
  },

  data() {
    return {
      albums: [],
      loading: true,
    };
  },

  async created() {
    this.loading = true;

    let albums = await AlbumService.getAllAlbums(true);
    this.albums = albums.filter((album) => album.access_level > 0);

    this.loading = false;
  },
};
</script>
