<template>
  <li>
    <router-link :to="{name: route, params: {path: album.path}}" :title="album.name">
      <div class="album-list-dc-row clearfix">
        <div class="album-list-dc-cover">
          <img
              v-if="album.cover !== null"
              :src="album.cover.thumbnail"
              :title="album.name"
              alt="Album cover"
          >
          <div v-else>
            <img
                :src="placeholder"
                :title="album.name"
                alt="Album cover placeholder image"
            >
            <div class="note album-no-cover-note">No cover</div>
          </div>
        </div>

        <div class="album-list-dc-details">
          <h3>{{ album.name }}</h3>

          <ul>
            <li v-html="date"></li>
            <!-- TODO: Photo and album counts -->
            <li>
              <span v-if="fullLocation">{{ fullLocation }}</span>
              <span v-else class="note">No location</span>
            </li>
          </ul>

          <div class="note" v-html="album.description"></div>
        </div>
      </div>
    </router-link>

    <AlbumListDetailedCards
        v-if="album.children"
        class="album-list-dc-items"
        :albums="album.children"
        :route="route"
    />
  </li>

</template>

<script>
  import AlbumListDetailedCards from "./AlbumListDetailedCards.vue";
  import {staticFiles} from "../store/editor";


  export default {
    components: {
      AlbumListDetailedCards
    },

    computed: {
      date() {
        if (this.album.end === null) {
          return this.album.start;
        } else {
          return "{0} &ndash; {1}".format(this.album.start, this.album.end)
        }
      },

      fullLocation() {
        let place = this.album.place;
        let location = this.album.location;

        if (place && location) {
          return "{0}, {1}".format(place, location);
        }

        return place || location || "";
      },

      placeholder() {
        return staticFiles.coverPlaceholder;
      },
    },

    filters: {
      pluralize(value) {
        return value === 1 ? '' : 's';
      },
    },

    name: "AlbumDetailedCard",

    props: {
      album: {
        type: Object,
        required: true,
      },
      route: {
        type: String,
        default: "album",
      },
    },
  };
</script>
