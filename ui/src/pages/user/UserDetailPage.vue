<template>
  <div v-if="!loading">
    <FixedWidthContainer>
      <h2>{{ user.name }}</h2>

      <ul>
        <li>Account created: {{ user.accountCreated }}</li>
        <li>Last sign in: {{ user.lastSignIn }}</li>
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
    this.$store.commit("setTitle", this.$route.params.slug);
    this.$store.commit("setBreadcrumbs", [
      {
        label: this.$route.params.slug,
        to: { name: "user", params: { slug: this.$route.params.slug } },
      },
    ]);

    this.loading = true;
    this.albums = await AlbumService.getAlbumsForUser(this.user.id);
    this.loading = false;
  },
};
</script>
