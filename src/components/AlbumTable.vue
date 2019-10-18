<template>
  <table class="album-table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Start</th>
        <th>End</th>
        <th>Location</th>
        <th class="album-table-tags">Tags</th>
        <th>Access</th>
      </tr>
    </thead>
    <tbody>
      <AlbumTableRow
          v-for="(album, index) in albums"
          :album="album"
          :isVisible="indexStart <= index && index <= indexEnd"
          :key="album.path.join('/')"
          :route="route"
      />
    </tbody>
  </table>
</template>

<script>
  import AlbumTableRow from "./AlbumTableRow.vue";


  export default {
    components: {
      AlbumTableRow,
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
  }
</script>

<style lang="scss">
  .album-table {
    border-collapse: collapse;
    width: 100%;

    th {
      padding: 12px 6px;
      background-color: rgb(0, 120, 255);
      color: white;
      text-align: center;
    }

    tr {
      &:nth-child(odd) {
        background-color: rgb(40, 40, 40);
      }

      &:nth-child(even) {
        background-color: rgb(60, 60, 60);
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
