<template>
  <div class="info-links">
    <h2>Navigation</h2>

    <dl title="Links">
      <div>
        <dt title="Album"><i class="fas fa-fw fa-book"></i></dt>
        <dd>
          <router-link :to="albumRoute">Return to album</router-link>
        </dd>
      </div>

      <div>
        <dt title="Album list"><i class="fas fa-fw fa-list"></i></dt>
        <dd>
          <router-link :to="{ name: 'index' }">Return to index</router-link>
        </dd>
      </div>
    </dl>
  </div>
</template>

<script>
export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
    isExternal: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    albumRoute() {
      return {
        name: this.isExternal ? "externalAlbum" : "album",
        params: {
          path: this.album.pathSplit,
        },
        query: {
          code: this.$route.query.code,
        },
      };
    },
  },
};
</script>

<style scoped>
i {
  margin-right: 6px;
}
</style>
