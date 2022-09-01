<template>
  <table>
    <thead>
      <tr>
        <th>Key</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Width</td>
        <td>{{ photo.width }}</td>
      </tr>
      <tr>
        <td>Height</td>
        <td>{{ photo.height }}</td>
      </tr>
      <tr>
        <td>Taken</td>
        <td>{{ photo.taken }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "PhotoMetadataTable",
  props: {
    photo: {
      type: Object,
      required: true,
    },
  },
};
</script>
