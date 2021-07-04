<template>
  <li class="nav-item">
    <h1 class="logo">
      <router-link
        class="nav-item-link"
        title="Doktor Takes Photos"
        :to="{ name: 'index' }"
      >
        Doktor Takes Photos
      </router-link>
    </h1>
  </li>
</template>

<script>
export default {
  name: "NavlinksLogo",
};
</script>
