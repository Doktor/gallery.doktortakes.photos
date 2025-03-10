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

  margin-bottom: 1rem;
}

.album-search-input {
  background-color: variables.$background-color;
  border: 1px solid variables.$background-color-3;
  border-radius: 0;

  height: 3.2rem;
  padding: 6px 12px;

  @include variables.text-font();
  color: variables.$text-color;
  font-size: 1.5rem;

  &::placeholder {
    color: variables.$text-color-2;
  }
}
</style>
