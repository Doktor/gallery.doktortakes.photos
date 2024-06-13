<template>
  <ul class="taxon-parents">
    <li v-for="item in parents" :key="item.catalogIdc">
      <router-link
        :to="{
          name: 'taxaByCatalogId',
          params: { catalogId: item.catalogId },
        }"
        >{{ item.name }}</router-link
      >
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    taxon: {
      type: Object,
      required: true,
    },
    taxaById: {
      type: Object,
      required: true,
    },
  },

  computed: {
    parents() {
      let ret = [];
      let taxon = this.taxon;

      while (taxon !== undefined) {
        ret.push(taxon);
        taxon = this.taxaById[taxon.passthroughParentCatalogId];
      }

      return ret.reverse();
    },
  },
};
</script>

<style lang="scss">
.taxon-parents {
  list-style-type: none;

  padding: 0;
  margin: 0;

  li {
    display: inline-block;

    &:not(:last-child)::after {
      content: "/";
      margin: 0 10px;
    }
  }
}
</style>
