<template>
  <div class="info-metadata">
    <h2>Metadata</h2>

    <dl title="Metadata">
      <div>
        <dt><i title="Sequence number" class="fas fa-fw fa-list-ol"></i></dt>
        <dd>{{ photo.index + 1 }} / {{ count }}</dd>
      </div>

      <div>
        <dt><i title="Taken at (date)" class="fas fa-fw fa-clock"></i></dt>
        <dd>{{ photo.takenDate }}</dd>
      </div>

      <div>
        <dt><i title="Taken at (time)" class="fas fa-fw fa-clock"></i></dt>
        <dd>{{ photo.takenTime }}</dd>
      </div>

      <div>
        <dt><i title="Dimensions" class="fas fa-fw fa-image"></i></dt>
        <dd>{{ image.width }} &times; {{ image.height }}</dd>
      </div>

      <div>
        <dt>
          <i
            title="Open in new tab"
            class="fas fa-fw fa-external-link-square-alt"
          ></i>
        </dt>
        <dd>
          <a
            :href="image.url"
            title="Open in new tab"
            target="_blank"
            rel="noopener noreferrer nofollow"
            >Open in new tab</a
          >
        </dd>
      </div>

      <div v-if="isStaff">
        <dt><i title="Admin" class="fas fa-fw fa-toolbox"></i></dt>
        <dd><a :href="adminUrl" title="Open in admin site">Admin</a></dd>
      </div>
    </dl>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useStore } from "@/store";

export default {
  props: {
    photo: {
      type: Object,
      required: true,
    },
    count: {
      type: Number,
      required: true,
    },
  },

  computed: {
    ...mapState(useStore, ["isStaff"]),
    ...mapState(useStore, ["user"]),

    adminUrl() {
      return `/redirect/admin/photos/${this.photo.md5}`;
    },

    image() {
      return this.photo.images.display ?? this.photo.images.original;
    },
  },
};
</script>

<style scoped>
i {
  margin-right: 6px;
}
</style>
