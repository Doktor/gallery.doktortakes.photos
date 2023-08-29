<template>
  <ul class="album-edit-links">
    <li>
      <a :href="album.url" title="View album" target="_blank">View</a>
    </li>
    <li>
      <a :href="album.admin_url" title="View album on admin site">Admin</a>
    </li>
    <li>
      <a
        :href="urlProductionSite"
        title="View album on production site"
        target="_blank"
        rel="noopener noreferrer"
        >Production</a
      >
    </li>
    <li>
      <a
        :href="urlAlphaSite"
        title="View album on alpha site"
        target="_blank"
        rel="noopener noreferrer"
        >Alpha</a
      >
    </li>
  </ul>
</template>

<script>
import { domains } from "../../constants";

export default {
  name: "AlbumLinks",
  props: {
    album: {
      type: Object,
      required: true,
    },
  },

  computed: {
    urlAlphaSite() {
      return new URL(this.album.url, domains.alpha).href;
    },

    urlProductionSite() {
      return new URL(this.album.url, domains.production).href;
    },
  },
};
</script>

<style lang="scss">
.album-edit-links {
  list-style: none;
  margin: 0;
  padding: 0;

  li {
    @include headings-font();

    display: inline-block;
  }

  li:not(:last-child)::after {
    color: $text-color;
    content: "/";
    margin: 0 0.75rem;
    position: relative;
  }
}
</style>
