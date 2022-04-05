<template>
  <h1 class="index-logo">Doktor Takes Photos</h1>
</template>

<script>
export default {
  name: "IndexLogo",
};
</script>

<style lang="scss" scoped>
.index-logo {
  @include logo-font();

  font-size: $index-logo-size;
  line-height: 1;
  text-align: center;
  text-transform: capitalize;

  padding: 0;
  margin: 0;
  margin-bottom: 1.2rem;

  @media (min-width: 901px) {
    font-size: $index-logo-size * 1.2;
    text-align: left;
  }
}
</style>
