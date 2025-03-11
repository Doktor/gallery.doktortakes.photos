<template>
  <div class="overlay-container" :class="classes">
    <div class="overlay-section">
      <div class="overlay-item">
        <h2 v-if="!isSkeleton" class="title">{{ album.name }}</h2>
        <h2 v-else class="title">Loading...</h2>
      </div>

      <div class="overlay-item" v-if="!loading">
        <span v-html="date"></span>

        <template v-if="count > 0">
          <span> &middot; </span>
          <span>{{ count }} photo{{ pluralize(count) }}</span>
        </template>
      </div>
    </div>

    <div class="overlay-section" v-if="!loading">
      <AlbumMetadata class="overlay-item" :album="album" />

      <div v-if="album.license" class="overlay-item">
        <i title="License" class="fas fa-fw fa-copyright"></i>

        <span :title="album.license.fullName || album.license.displayName">
          <a
            v-if="album.license.link"
            :href="album.license.link"
            target="_blank"
            rel="noopener noreferrer nofollow"
            >{{ album.license.displayName }}
          </a>
          <template v-else>{{ album.license.displayName }}</template>
        </span>
      </div>

      <AlbumAccessInfo class="overlay-item" :album="album" />
      <AlbumLinks
        class="overlay-item"
        v-if="isStaff"
        :album="album"
        :showManage="showManage"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import AlbumAccessInfo from "./AlbumAccessInfo";
import AlbumLinks from "@/components/albumDetail/AlbumLinks";
import AlbumMetadata from "./AlbumMetadata";
import { pluralize } from "@/utils";

function toFullDateTimeForm(dateForm) {
  return `${dateForm}T00:00:00+00:00`;
}

function formatDate(dateString) {
  return new Date(toFullDateTimeForm(dateString)).toLocaleString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

export default {
  components: {
    AlbumAccessInfo,
    AlbumLinks,
    AlbumMetadata,
  },

  computed: {
    ...mapGetters(["isStaff"]),
    ...mapState(["loading", "user"]),

    classes() {
      return {
        "is-empty": !this.isSkeleton && this.album.cover === null,
        "is-skeleton": this.isSkeleton,
      };
    },

    date() {
      let start = this.album.start;
      let end = this.album.end;

      return end === null
        ? formatDate(start)
        : `${formatDate(start)} &ndash; ${formatDate(end)}`;
    },
  },

  methods: {
    pluralize,
  },

  props: {
    album: {
      type: Object,
      required: true,
    },
    count: {
      type: Number,
      required: true,
    },
    isSkeleton: {
      type: Boolean,
      default: false,
    },
    showManage: {
      type: Boolean,
      default: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.overlay-container {
  position: relative;
  z-index: 1;
  min-height: math.div(100vh, 3);

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  background-color: rgba(variables.$background-color, 0.6);

  &.is-empty,
  &.is-skeleton {
    min-height: unset;
    background-color: unset;
  }
}

.overlay-section {
  padding: 1.8rem;
}

.title {
  display: inline-block;
  margin: 0;

  font-size: 3.3rem;
  text-transform: none;
}

.overlay-item,
:deep(.overlay-item) {
  @include variables.sidebar-font();
  font-size: 1.5rem;
  text-align: left;
  text-transform: none;

  margin-bottom: 1rem;

  i {
    margin-right: 6px;
  }

  &:last-child {
    margin-bottom: 0;
  }
}
</style>
