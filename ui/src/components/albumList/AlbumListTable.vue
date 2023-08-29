<template>
  <table class="album-table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Date</th>
        <th>Location</th>
        <th class="album-table-tags">Tags</th>
        <th>Access</th>
        <th>Owners</th>
      </tr>
    </thead>
    <tbody>
      <AlbumListTableRow
        v-for="(album, index) in albums"
        :album="album"
        :isVisible="indexStart <= index && index <= indexEnd"
        :key="album.path"
        :route="route"
      />
    </tbody>
  </table>
</template>

<script>
import AlbumListTableRow from "./AlbumListTableRow.vue";

export default {
  components: {
    AlbumListTableRow,
  },

  props: {
    albums: {
      type: Array,
      required: true,
    },
    route: {
      type: String,
      default: "album",
    },

    indexStart: {
      type: Number,
      required: true,
    },
    indexEnd: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.album-table {
  border-collapse: collapse;
  width: 100%;

  th {
    padding: 12px 6px;
    background-color: $text-blue;
    color: white;
    text-align: center;
  }

  tr {
    &:nth-child(odd) {
      background-color: $background-color-2;
    }

    &:nth-child(even) {
      background-color: $background-color-3;
    }
  }

  td {
    padding: 6px 12px;
  }
}

.album-table-tags {
  max-width: 300px;
  word-wrap: break-spaces;
}
</style>
