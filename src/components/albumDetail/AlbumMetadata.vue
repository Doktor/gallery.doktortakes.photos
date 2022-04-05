<template>
  <div>
    <div v-if="location" class="overlay-item">
      <i title="Location" class="fas fa-fw fa-map-marker-alt"></i>
      <span>{{ location }}</span>
    </div>

    <div v-if="album.tags.length > 0" class="overlay-item">
      <i title="Tags" class="fas fa-fw fa-tags"></i>
      <span>
        <template v-for="(slug, index) in album.tags">
          <router-link
            class="tag"
            :key="slug"
            :to="{ name: 'tag', params: { slug: slug } }"
            ><!--
              -->#{{ slug
            }}<!--
            --></router-link
          >
          <span
            v-if="index !== album.tags.length - 1"
            v-html="nbsp"
            :key="'space-' + index.toString()"
          ></span>
        </template>
      </span>
    </div>

    <div v-if="album.description" class="overlay-item">
      <i title="Description" class="fas fa-fw fa-book"></i>
      <span v-html="album.description"></span>
    </div>

    <div v-if="album.parent" class="overlay-item">
      <i title="Parent album" class="fas fa-fw fa-chevron-circle-up"></i>
      <router-link
        :to="{ name: 'album', params: { path: album.parent.split('/') } }"
        ><!--
        -->View parent album<!--
      --></router-link>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
  },

  computed: {
    ...mapState(["photos", "user"]),

    location() {
      let place = this.album.place;
      let location = this.album.location;

      if (place && location) {
        return "{0}, {1}".format(place, location);
      }

      return place || location || "";
    },

    nbsp() {
      return "&nbsp;";
    },
  },
};
</script>
