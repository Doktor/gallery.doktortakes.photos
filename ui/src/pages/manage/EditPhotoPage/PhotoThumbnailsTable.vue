<template>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Width</th>
        <th>Height</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="(thumbnail, index) in thumbnails" :key="index">
        <td>
          <a :href="thumbnail.url">
            <span v-if="thumbnail.type">{{ thumbnail.type }}</span>
            <i v-else>(untitled)</i>
          </a>
        </td>
        <td>{{ thumbnail.width }}</td>
        <td>{{ thumbnail.height }}</td>
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
