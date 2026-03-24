<template>
  <FixedWidthContainer>
    <h2>Change your password</h2>

    <div class="password-form-container">
      <PasswordForm @success="redirect" />
    </div>
  </FixedWidthContainer>
</template>

<script>
import { useStore } from "@/store";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import PasswordForm from "@/components/user/PasswordForm";
import { sleep } from "@/utils";
import { router } from "@/router";

export default {
  components: {
    FixedWidthContainer,
    PasswordForm,
  },

  created() {
    const store = useStore();
    const slug = store.user.name;

    store.setBreadcrumbs([
      { label: slug, to: { name: "user", params: { slug } } },
      {
        label: "Change password",
        to: { name: "changePassword", params: { slug } },
      },
    ]);
  },

  methods: {
    async redirect() {
      await sleep(1000);

      await router.push({
        name: "user",
        params: {
          slug: useStore().user.name,
        },
      });
    },
  },
};
</script>

<style scoped>
h2 {
  text-align: center;
}
</style>
