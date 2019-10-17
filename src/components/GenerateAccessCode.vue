<template>
  <div class="form-link-action">
    <a @click.prevent="generateCode">Generate access code</a>
  </div>
</template>

<script>
  const hex = '0123456789abcdef';

  function randomInt(min, max) {
    // Generates a random integer in the range [min, max]
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }


  export default {
    methods: {
      generateCode() {
        let arr = [];

        for (let i = 0; i < 32; i++) {
          arr.push(hex.charAt(randomInt(0, hex.length - 1)));
        }

        this.$emit('set-access-code', arr.join(''));
      }
    }
  }
</script>
