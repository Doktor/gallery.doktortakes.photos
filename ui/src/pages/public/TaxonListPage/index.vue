<template>
  <FixedWidthContainer v-if="!loading">
    <TaxonParents
      v-if="catalogId"
      :taxon="selectedTaxon"
      :taxaById="taxaById"
    />
    <TaxaChildren :items="taxa" />

    <template v-if="!loadingPhotos">
      <PhotoGallery v-if="photos.length > 0" :photos="photos" />
      <div v-else>There are no photos of this taxon.</div>
    </template>
  </FixedWidthContainer>
</template>

<script>
import { TaxaService } from "@/services/TaxaService";
import TaxaChildren from "./TaxaChildren";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import TaxonParents from "./TaxonParents";
import PhotoGallery from "@/components/photoList/PhotoGallery.vue";
import { TaxonPhotoService } from "@/services/TaxonPhotoService";

const ranks = [
  "domain",
  "kingdom",
  "phylum",
  "class",
  "order",
  "family",
  "genus",
  "species",
].reverse();

export default {
  name: "TaxonListPage",
  components: { PhotoGallery, TaxonParents, FixedWidthContainer, TaxaChildren },

  data() {
    return {
      loading: true,
      taxa: [],

      taxaById: {},
      taxaByRank: {},

      loadingPhotos: true,
      photos: [],
    };
  },

  computed: {
    catalogId() {
      return this.$route.params.catalogId;
    },
    selectedTaxon() {
      return this.taxa[0];
    },
  },

  methods: {
    async loadPhotos() {
      this.loadingPhotos = true;

      let { ok, content } = await TaxonPhotoService.get(
        this.selectedTaxon.catalogId,
        true,
      );

      if (ok) {
        this.photos = content;
      } else {
        this.$store.commit("addNotification", {
          message: "An error occurred when retrieving photos for this taxon.",
          status: "error",
        });
      }

      this.loadingPhotos = false;
    },
  },

  watch: {
    catalogId: {
      async handler(newCatalogId) {
        if (newCatalogId) {
          this.taxa = [this.taxaById[newCatalogId]];
          await this.loadPhotos();
        } else {
          this.taxa = this.taxaByRank["kingdom"];
        }
      },
    },
  },

  async mounted() {
    this.loading = true;

    let taxa = await TaxaService.getTaxa();

    for (let taxon of taxa) {
      this.taxaById[taxon.catalogId] = taxon;
    }

    for (let rank of ranks) {
      this.taxaByRank[rank] = taxa.filter((t) => t.rank === rank);
    }

    for (let i = 1; i < ranks.length; i++) {
      let rank = ranks[i];
      let rankBelow = ranks[i - 1];

      for (let taxon of this.taxaByRank[rank]) {
        taxon.children = this.taxaByRank[rankBelow].filter(
          (t) => taxon.catalogId === t.passthroughParentCatalogId,
        );
      }
    }

    if (this.catalogId) {
      this.taxa = [this.taxaById[this.catalogId]];
      await this.loadPhotos();
    } else {
      this.taxa = this.taxaByRank["kingdom"];
    }

    this.loading = false;
  },
};
</script>
