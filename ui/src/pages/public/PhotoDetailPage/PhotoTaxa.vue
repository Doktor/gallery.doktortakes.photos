<template>
  <div>
    <h2>Species</h2>

    <ul>
      <li v-for="taxon in taxa">
        <router-link
          :to="{
            name: 'taxaByCatalogId',
            params: { catalogId: taxon.catalog_id },
          }"
        >
          {{ taxon.name }}
        </router-link>
        &mdash; {{ taxon.common_name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    taxa: {
      type: Array,
      required: true,
    },
  },
};
</script>
