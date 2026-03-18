<template>
  <main>
    <AlbumGallery :albums="albums" :showCount="false" :loading="loading" />
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { AlbumService } from "@/services/AlbumService";
import AlbumGallery from "@/components/albumList/AlbumGallery.vue";

const albums = ref([]);

onMounted(async () => {
  albums.value = await AlbumService.getExternalAlbums();
});
</script>

<style scoped lang="scss"></style>
