<template>
  <tr :class="{'hidden': !this.isVisible}">
    <td>
      <router-link :title="album.name" :to="{name: route, params: {path: album.path}}">
        {{ album.name }}
      </router-link>
    </td>
    <td>{{ album.start }}</td>
    <td>{{ album.end }}</td>
    <td>{{ fullLocation }}</td>
    <td class="album-table-tags">
      <template v-for="(slug, index) in album.tags">
        <router-link class="tag" :to="{name: 'tag', params: {slug: slug}}">#{{ slug }}</router-link>
        <span v-if="index !== album.tags.length - 1" v-html="' '"></span>
      </template>
    </td>
    <td>{{ album.access_level }}</td>
  </tr>
</template>

<script>
  export default {
    computed: {
      fullLocation() {
        let place = this.album.place;
        let location = this.album.location;

        if (place && location) {
          return "{0}, {1}".format(place, location);
        }

        return place || location || "";
      },
    },

    props: {
      album: {
        type: Object,
        required: true,
      },
      route: {
        type: String,
        default: "album",
      },

      isVisible: {
        type: Boolean,
        required: true,
      },
    }
  }
</script>
