<template>
  <header class="sidebar-header">
    <h1 class="sidebar-logo">
      <router-link
        class="sidebar-logo-link"
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
  name: "SidebarHeader",
};
</script>

<style lang="scss" scoped>
.sidebar-header {
  margin-bottom: variables.$sidebar-margin;
}

.sidebar-logo {
  @include variables.logo-font();
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

.sidebar-logo-link {
  color: variables.$text-blue;
  text-decoration: none;
}
</style>
