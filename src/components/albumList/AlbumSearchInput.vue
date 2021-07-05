<template>
  <div class="album-search-input">
    <input
      type="text"
      placeholder="Search by name..."
      :value="value"
      @input="$emit('input', $event.target.value)"
    />
  </div>
</template>

<script>
export default {
  name: "AlbumSearchInput",

  data() {
    return {
      value: "",
    };
  },
};
</script>

<style lang="scss" scoped>
.album-search-input {
  width: 100%;
  margin: 1rem 0;

  input {
    background-color: $background-color;
    border: 1px solid $text-color;

    height: 3.2rem;
    padding: 6px 12px;

    @include headings-font();
    color: $text-color;
    font-size: 1.5rem;
    line-height: 1;
  }
}
</style>
