<template>
  <header class="nav-header">
    <h1 class="nav-logo">
      <router-link
        class="nav-logo-link"
        title="Doktor Takes Photos"
        :to="{ name: 'index' }"
      >
        <div>Doktor</div>
        <div>Takes</div>
        <div>Photos</div>
      </router-link>
    </h1>
  </header>
</template>

<script>
export default {
  name: "NavHeader",
};
</script>

<style lang="scss" scoped>
.nav-header {
  margin-bottom: variables.$sidebar-margin;
}

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
}

.nav-logo-link {
  color: variables.$text-blue;
  text-decoration: none;
}
</style>
