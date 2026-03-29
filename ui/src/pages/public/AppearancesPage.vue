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
import { useStore } from "@/store";

const store = useStore();
const albums = ref([]);

onMounted(async () => {
  store.setLoading(true);

  albums.value = await AlbumService.getExternalAlbums();

  useStore().setBreadcrumbs([
    {
      label: "Appearances",
      to: { name: "externalAlbums" },
    },
  ]);

  store.setLoading(false);
});
</script>

<style scoped lang="scss"></style>
