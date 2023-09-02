<template>
  <table>
    <thead>
      <tr>
        <th>Key</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="[key, value] in Object.entries(photo.exif)" :key="key">
        <td>{{ key }}</td>
        <td>{{ value }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "PhotoExifTable",
  props: {
    photo: {
      type: Object,
      required: true,
    },
  },
};
</script>
