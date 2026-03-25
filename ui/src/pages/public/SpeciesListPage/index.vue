<template>
  <main v-if="!loading">
    <div class="container">
      <div
        class="wrapper"
        v-for="{ taxon, photos } in species"
        :key="taxon.catalogId"
      >
        <router-link
          :to="{
            name: 'taxaByCatalogId',
            params: { catalogId: taxon.catalogId },
          }"
        >
          <PhotoThumbnail :isLoading="false" :photo="photos[0]" />
        </router-link>
        <div class="subtitle">{{ taxon.commonName.toLowerCase() }}</div>
      </div>
    </div>
  </main>
</template>

<script>
import { useStore } from "@/store";
import { TaxaService } from "@/services/TaxaService";
import PhotoThumbnail from "@/components/photoList/PhotoThumbnail.vue";

export default {
  components: { PhotoThumbnail },

  data() {
    return {
      loading: true,
      species: [],
    };
  },

  created() {
    useStore().setBreadcrumbs([
      {
        label: "Species",
        to: { name: "species" },
      },
    ]);
  },

  async mounted() {
    this.loading = true;
    this.species = await TaxaService.getSpecies();
    this.loading = false;
  },
};
</script>

<style lang="scss">
@use "@/styles/variables";

.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  grid-gap: 10px;
}

.wrapper {
  width: 100%;

  position: relative;
}

.subtitle {
  position: absolute;
  bottom: 10px;
  left: 10px;

  color: white;
  background-color: rgba(0, 0, 0, 0.6);

  padding: 4px 12px;
  border-radius: 2px;

  @include variables.headings-font();
  font-weight: 400 !important;
}
</style>
