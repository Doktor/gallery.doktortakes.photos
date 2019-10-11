<template>
  <ul>
    <template v-for="(album, index) in albums">
      <li v-if="indexStart <= index && index <= indexEnd">
        <router-link
            :to="{name: route, params: {path: album.path}}"
            :title="album.name"
            :href="album.url"
        >
          {{ album.name }}
        </router-link>

        <AlbumListSimple v-if="album.children" :albums="album.children" :route="route"/>
      </li>
    </template>
  </ul>
</template>

<script>
  export default {
    name: "AlbumListSimple",

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
      },
      indexEnd: {
        type: Number,
      },
    },
  }
</script>
