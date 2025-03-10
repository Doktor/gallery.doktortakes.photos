<template>
  <li class="nav-section">
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
  line-height: 1;

  margin: 0;
  padding: 0;
  padding-bottom: 4px;

  .nav-item-link {
    @include variables.logo-font();

    color: variables.$text-blue;
    font-size: variables.$nav-logo-size;
    line-height: 1;
    text-align: center;

    @media (min-width: 901px) {
      font-size: variables.$nav-logo-size * 1.15;
    }
  }
}
</style>
