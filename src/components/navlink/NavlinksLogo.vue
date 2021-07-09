<template>
  <li class="nav-item">
    <h1 class="nav-logo">
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

<style lang="scss" scoped>
.nav-logo {
  @include logo-font();

  color: $text-color;
  font-size: $nav-logo-size;
  line-height: 1;
  text-align: center;
  text-transform: capitalize;

  padding: 0;
  margin: 0;

  @media (min-width: 901px) {
    font-size: $nav-logo-size * 1.15;
  }
}
</style>
