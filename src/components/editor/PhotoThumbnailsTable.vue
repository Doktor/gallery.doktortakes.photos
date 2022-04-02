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
        <td>
          <span v-if="thumbnail.type">{{ thumbnail.type }}</span>
          <i v-else>(untitled)</i>
        </td>
        <td>{{ thumbnail.width }}x{{ thumbnail.height }}</td>
        <td>
          <a :href="thumbnail.url">{{ thumbnail.name }}</a>
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
