<template>
  <FixedWidthContainer>
    <router-link :to="{name: 'editorIndex'}">Back to editor</router-link>
    <h2>Create new album</h2>
    <AlbumForm
        class="form--small"
        :save-button-text="'Create album'"
        :update="false"
    />
  </FixedWidthContainer>
</template>

<script>
  import AlbumForm from '@/components/editor/AlbumForm.vue';
  import FixedWidthContainer from "@/components/FixedWidthContainer";
  import {mapState} from 'vuex';


  export default {
    components: {
      AlbumForm,
      FixedWidthContainer,
    },

    computed: {
      ...mapState([
        'album',
      ]),
    },

    created() {
      this.$store.commit('clearAlbum');
    }
  }
</script>
