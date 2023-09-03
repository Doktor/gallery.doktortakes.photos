<template>
  <ul class="taxa-list">
    <li v-for="item in items" :key="item.catalog_id">
      <span>
        {{ item.name }}
        <template v-if="item.common_name"
          >&mdash; <em>{{ item.common_name.toLowerCase() }}</em>
        </template>
      </span>

      <TaxaList
        v-if="item.children?.length > 0 ?? false"
        :items="item.children"
      />
    </li>
  </ul>
</template>

<script>
export default {
  name: "TaxaList",

  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style>
.taxa-list {
  margin: 0;
  text-align: left;
}
</style>
