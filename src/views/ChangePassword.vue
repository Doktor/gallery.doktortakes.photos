<template>
  <section>
    <h2>Change your password</h2>

    <div class="password-form-container">
      <PasswordForm/>
    </div>
  </section>
</template>

<script>
  import PasswordForm from "../components/PasswordForm.vue";

  export default {
    components: {
      PasswordForm,
    },

  }
</script>

<style scoped>
  h2 {
    text-align: center;
  }
</style>
