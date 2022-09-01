<template>
  <div class="album-search-container">
    <input
      class="album-search-input"
      type="text"
      placeholder="Search albums by name"
      :value="value"
      @input="$emit('input', $event.target.value)"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      value: "",
    };
  },
};
</script>

<style lang="scss" scoped>
.album-search-container {
  width: 100%;
  max-width: 500px;

  margin: 1rem 0;
}

.album-search-input {
  background-color: $background-color;
  border: 1px solid $background-color-3;
  border-radius: 0;

  height: 3.2rem;
  padding: 6px 12px;

  @include secondary-headings-font();
  color: $text-color;
  font-size: 1.5rem;
  line-height: 1;

  &::placeholder {
    color: $text-color-2;
  }
}
</style>
