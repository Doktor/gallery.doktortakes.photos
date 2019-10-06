<template>
  <ul>
    <li v-for="album in albums">
      <router-link
          :to="{name: 'album', params: {path: album.path}}"
          :title="album.name"
          :href="album.url"
      >
        {{ album.name }}
      </router-link>

      <AlbumListSimple v-if="album.children" :albums="album.children"/>
    </li>
  </ul>
</template>

<script>
  export default {
    name: "AlbumListSimple",

    props: {
      albums: Array,
      required: true,
    },
  }
</script>
