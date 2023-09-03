<template>
  <FixedWidthContainer>
    <TaxaList :items="taxa" />
  </FixedWidthContainer>
</template>

<script>
import { TaxaService } from "@/services/TaxaService";
import { sleep, withLoading } from "@/utils";
import TaxaList from "./TaxaList";
import FixedWidthContainer from "@/components/FixedWidthContainer";

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
  components: { FixedWidthContainer, TaxaList },
  data() {
    return {
      loading: true,
      taxa: [],
    };
  },

  async mounted() {
    this.loading = true;
    let taxa = await TaxaService.getTaxa();
    this.loading = false;

    let taxaByRank = {};

    for (let rank of ranks) {
      taxaByRank[rank] = taxa.filter((t) => t.rank === rank);
    }

    console.log(taxaByRank);

    for (let i = 1; i < ranks.length; i++) {
      let rank = ranks[i];
      let rankBelow = ranks[i - 1];

      for (let taxon of taxaByRank[rank]) {
        taxon.children = taxaByRank[rankBelow].filter(
          (t) => taxon.catalog_id === t.passthrough_parent_catalog_id,
        );
      }
    }

    this.taxa = taxaByRank["kingdom"];
  },
};
</script>
