<template>
  <form class="form--1-column" v-on:submit.prevent="submit">
    <div class="form-control">
      <label for="f-username">Username</label>
      <input class="field" name="username" maxlength="150" id="f-username" type="text" v-model="username" required>
    </div>

    <div class="form-control">
      <label for="f-password">Password</label>
      <input class="field" name="password" maxlength="150" id="f-password" type="password" v-model="password" required>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <button type="submit">Log in</button>
  </form>
</template>

<script>
  import {router} from "@/router/main";

  export default {
    data() {
      return {
        username: "",
        password: "",
        error: "",
      }
    },

    computed: {
      redirect() {
        return this.$router.currentRoute.query?.redirect ?? null;
      }
    },

    methods: {
      async submit() {
        try {
          let {ok, content} = await this.$store.dispatch('authenticate', {
            username: this.username,
            password: this.password,
          });

          if (ok) {
            this.$store.commit('setApiToken', content.token);
            this.$store.commit('addTimedNotification', {message: "Logged in successfully.", hideAfter: 5000});
            await this.$store.dispatch('getUser');

            this.$store.commit('setAllAlbums', []);
            this.$store.commit('setAlbums', []);
            router.push(this.redirect ?? {name: 'albums'});
            return
          }

          this.error = content.error
        } catch {
          this.error = "An unspecified error occured.";
        }
      },
    },

    async mounted() {
      await this.$store.dispatch('ensureCsrfToken');
    },
  }
</script>

<style lang="scss" scoped>
.error {
  color: $text-error;
  line-height: 1;
  margin: 1rem 0;
}
</style>
