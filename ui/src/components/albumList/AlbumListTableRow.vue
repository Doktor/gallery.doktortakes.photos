<template>
  <tr :class="{ hidden: !this.isVisible }">
    <td>
      <router-link
        :title="album.name"
        :to="{ name: route, params: { pathArray: album.pathArray } }"
      >
        {{ album.name }}
      </router-link>
    </td>
    <td>
      {{ album.start
      }}<template v-if="album.end"> &ndash; {{ album.end }}</template>
    </td>
    <td>{{ fullLocation }}</td>
    <td class="album-table-tags">
      <template v-for="(slug, index) in album.tags">
        <router-link class="tag" :to="{ name: 'tag', params: { slug: slug } }"
          >#{{ slug }}</router-link
        >
        <span v-if="index !== album.tags.length - 1" v-html="' '"></span>
      </template>
    </td>
    <td>{{ album.accessLevel }}</td>
    <td>
      <template v-if="album.users?.length > 0 ?? false">
        <strong>Users:</strong> {{ album.users.join(", ") }}
      </template>
      <template v-if="album.users && album.groups"><br /></template>
      <template v-if="album.groups?.length > 0 ?? false">
        <strong>Groups:</strong> {{ album.groups.join(", ") }}
      </template>
    </td>
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
  },
};
</script>
