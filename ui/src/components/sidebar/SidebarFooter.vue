<template>
  <footer class="sidebar-footer">
    <div class="sidebar-tagline">:3</div>

    <div>
      website & photos
      <router-link :to="{ name: 'copyright' }">&copy; Doktor</router-link>
    </div>
  </footer>
</template>

<style lang="scss">
@use "@/styles/variables";

.sidebar-tagline {
  @include variables.headings-font();
  color: variables.$text-color;
  font-weight: 400;

  margin: 1rem 0;
  width: 100%;
}
</style>
