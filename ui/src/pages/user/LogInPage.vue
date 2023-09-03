<template>
  <form class="form--1-column" @submit.prevent="submit">
    <CustomInput label="Username" v-model="username" maxlength="150" required />
    <CustomInput
      label="Password"
      type="password"
      v-model="password"
      maxlength="150"
      required
    />

    <div v-if="error" class="error">{{ error }}</div>

    <CustomButton class="button-primary" type="submit">Log in</CustomButton>
  </form>
</template>

<script>
import { router } from "@/router";
import CustomInput from "@/components/form/CustomInput";
import CustomButton from "@/components/form/CustomButton";

export default {
  components: { CustomButton, CustomInput },
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },

  computed: {
    redirect() {
      return this.$router.currentRoute.query?.redirect ?? null;
    },
  },

  methods: {
    async submit() {
      try {
        let { ok, content } = await this.$store.dispatch("authenticate", {
          username: this.username,
          password: this.password,
        });

        if (ok) {
          this.$store.commit("setApiToken", content.token);
          this.$store.commit("addTimedNotification", {
            message: "Logged in successfully.",
            hideAfter: 5000,
          });
          await this.$store.dispatch("getUser");

          router.push(this.redirect ?? { name: "albums" });
          return;
        }

        this.error = content.error;
      } catch {
        this.error = "An unspecified error occured.";
      }
    },
  },

  async mounted() {
    await this.$store.dispatch("ensureCsrfToken");
  },
};
</script>

<style lang="scss" scoped>
.error {
  color: $text-error;
  line-height: 1;
  margin: 1rem 0;
}
</style>
