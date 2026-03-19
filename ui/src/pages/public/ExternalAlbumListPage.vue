<template>
  <main>
    <AlbumGallery
      :albums="albums"
      :showCount="false"
      :loading="store.loading"
      albumRoute="externalAlbum"
    />
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { AlbumService } from "@/services/AlbumService";
import AlbumGallery from "@/components/albumList/AlbumGallery.vue";
import { useStore } from "vuex";

const store = useStore();
const albums = ref([]);

onMounted(async () => {
  store.commit("setLoading", true);

  albums.value = await AlbumService.getExternalAlbums();

  store.commit("setLoading", false);
});
</script>

<style scoped lang="scss"></style>
