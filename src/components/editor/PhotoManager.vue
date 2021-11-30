<template>
  <section class="manage-photos">
    <h2>Manage photos</h2>

    <div>
      {{ photos.length }} photos in album,
      {{ selected.length }} photo{{ selected.length | pluralize }} selected
    </div>

    <div>
      <button
          @click="selectAll"
          type="button"
      >
        Select all
      </button>
      <button
          @click="selectNone"
          type="button"
      >
        Select none
      </button>
      <button
          @click="selectInvert"
          type="button"
      >
        Invert selection
      </button>
    </div>

    <div class="photo-actions">
      <div>
        <button @click="setAlbumCover">Set cover</button>
      </div>

      <div>
        <button
            @click="deleteSelected"
            type="button"
        >
          Delete
        </button>
      </div>
    </div>

    <p v-if="!photos.length">
      This album does not contain any photos.
    </p>
    <Photos v-else :photos="photos" :allowSelect="true" />
  </section>
</template>

<script>
import Photos from '@/components/photoList/Photos.vue';
import {mapActions, mapMutations, mapState} from 'vuex';


export default {
  components: {
    Photos,
  },

  props: {
    photos: {
      type: Array,
      required: true,
    },
  },

  computed: {
    ...mapState([
      'selected',
    ]),
  },

  filters: {
    pluralize(value) {
      return value === 1 ? '' : 's';
    },
  },

  methods: {
    ...mapActions([
      'deleteSelected',
      'setAlbumCover',
    ]),
    ...mapMutations([
      'selectAll',
      'selectInvert',
      'selectNone',
    ]),
  },
}
</script>
