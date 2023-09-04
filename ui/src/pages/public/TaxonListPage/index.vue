<template>
  <FixedWidthContainer v-if="!loading">
    <TaxonParents v-if="catalogId" :taxon="taxa[0]" :taxaById="taxaById" />
    <TaxaChildren :items="taxa" />
  </FixedWidthContainer>
</template>

<script>
import { TaxaService } from "@/services/TaxaService";
import TaxaChildren from "./TaxaChildren";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import TaxonParents from "./TaxonParents";

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
  components: { TaxonParents, FixedWidthContainer, TaxaChildren },

  data() {
    return {
      loading: true,
      taxa: [],

      taxaById: {},
      taxaByRank: {},
    };
  },

  computed: {
    catalogId() {
      return this.$route.params.catalogId;
    },
  },

  watch: {
    catalogId: {
      handler(newCatalogId) {
        if (newCatalogId) {
          this.taxa = [this.taxaById[newCatalogId]];
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
      this.taxaById[taxon.catalog_id] = taxon;
    }

    for (let rank of ranks) {
      this.taxaByRank[rank] = taxa.filter((t) => t.rank === rank);
    }

    for (let i = 1; i < ranks.length; i++) {
      let rank = ranks[i];
      let rankBelow = ranks[i - 1];

      for (let taxon of this.taxaByRank[rank]) {
        taxon.children = this.taxaByRank[rankBelow].filter(
          (t) => taxon.catalog_id === t.passthrough_parent_catalog_id,
        );
      }
    }

    if (this.catalogId) {
      this.taxa = [this.taxaById[this.catalogId]];
    } else {
      this.taxa = this.taxaByRank["kingdom"];
    }

    this.loading = false;
  },
};
</script>
