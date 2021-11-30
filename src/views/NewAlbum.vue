<template>
  <FixedWidthContainer>
    <router-link :to="{name: 'manage'}">Back to editor</router-link>
    <h2>Create new album</h2>
    <AlbumForm
        class="form--small"
        :album="album"
        :save-button-text="'Create album'"
        :update="false"
        @save="createAlbum"
    />
  </FixedWidthContainer>
</template>

<script>
  import AlbumForm from '@/components/editor/AlbumForm.vue';
  import FixedWidthContainer from "@/components/FixedWidthContainer";


  export default {
    components: {
      AlbumForm,
      FixedWidthContainer,
    },

    data() {
      return {
        album: {
          name: '',
          place: '',
          location: '',
          description: '',
          start: '',
          end: '',
          access_level: 0,
          access_code: '',
          parent: '',
        },
      }
    },

    methods: {
      createAlbum(album) {
        this.$store.dispatch('createAlbum', album);
      },
    },
  }
</script>
