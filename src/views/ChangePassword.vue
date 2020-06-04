<template>
  <FixedWidthContainer>
    <h2>Change your password</h2>

    <div class="password-form-container">
      <PasswordForm/>
    </div>
  </FixedWidthContainer>
</template>

<script>
  import FixedWidthContainer from "../components/FixedWidthContainer.vue";
  import PasswordForm from "../components/user/PasswordForm.vue";

  export default {
    components: {
      FixedWidthContainer,
      PasswordForm,
    },

  }
</script>

<style scoped>
  h2 {
    text-align: center;
  }
</style>
