<template>
  <ul class="taxa-children">
    <li v-for="item in items" :key="item.catalog_id">
      <span>
        <router-link
          :to="{
            name: 'taxaByCatalogId',
            params: { catalogId: item.catalog_id },
          }"
        >
          {{ item.name }}
        </router-link>
        <template v-if="item.common_name"
          >&mdash; <em>{{ item.common_name.toLowerCase() }}</em>
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
  text-align: left;
}
</style>
