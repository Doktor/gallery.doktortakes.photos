<template>
  <li class="nav-section">
    <h1 class="nav-logo">
      <router-link
        class="nav-item-link"
        title="Doktor Takes Photos"
        :to="{ name: 'index' }"
      >
        <div>Doktor</div>
        <div>Takes</div>
        <div>Photos</div>
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
  @include variables.logo-font();
  line-height: 1;
  text-align: center;

  margin: 0;
  padding: 0;
  padding-bottom: 8px;
  border-bottom: 8px solid variables.$text-blue;

  @media (min-width: 901px) {
    text-align: left;
    font-size: 3.5rem;
  }

  .nav-item-link {
    color: variables.$text-blue;
    text-decoration: none;
  }
}
</style>
