<template>
  <ul class="taxa-children">
    <li v-for="item in items" :key="item.catalogId">
      <span>
        <router-link
          :to="{
            name: 'taxaByCatalogId',
            params: { catalogId: item.catalogId },
          }"
        >
          {{ item.name }}
        </router-link>
        <template v-if="item.commonName"
          >&mdash; <em>{{ item.commonName.toLowerCase() }}</em>
        </template>
      </span>

      <TaxaChildren
        v-if="item.children?.length > 0 ?? false"
        :items="item.children"
      />
    </li>
  </ul>
</template>

<script>
export default {
  name: "TaxaChildren",

  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style>
.taxa-children {
  margin: 0;
  padding: 0 32px;
  text-align: left;
}
</style>
