<template>
  <div>
    <h2>Species</h2>

    <ul>
      <li v-for="taxon in taxa">
        <router-link
          :to="{
            name: 'taxaByCatalogId',
            params: { catalogId: taxon.catalogId },
          }"
        >
          {{ taxon.name }}
        </router-link>
        &mdash; {{ taxon.commonName }}
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
