<template>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Dimensions</th>
        <th>Link</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(thumbnail, index) in thumbnails" :key="index">
        <td>{{ thumbnail.type }}</td>
        <td>{{ thumbnail.width }}x{{ thumbnail.height }}</td>
        <td>
          <a :href="thumbnail.url">{{ thumbnail.url }}</a>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "PhotoThumbnailsTable",
  props: {
    thumbnails: {
      type: Array,
      required: true,
    },
  },
};
</script>
