<template>
  <form class="password-form form--1-column form--small">
    <fieldset>
      <CustomInput
        label="Current"
        type="password"
        autocomplete="off"
        v-model="current.value"
        @input="onEdit('current')"
        :errors="current.errors"
      />

      <CustomInput
        label="New password"
        type="password"
        autocomplete="off"
        v-model="password1.value"
        @input="onEdit('password1')"
        :errors="password1.errors"
        description="Your password must contain at least 8 characters."
      />

      <CustomInput
        label="Repeat password"
        type="password"
        autocomplete="off"
        v-model="password2.value"
        @input="onEdit('password2')"
        :errors="password2.errors"
      />
    </fieldset>

    <div class="form-buttons">
      <router-link
        class="form-button form-button-secondary"
        :to="{ name: 'user' }"
      >
        Cancel
      </router-link>

      <button
        class="form-button form-button-primary"
        type="submit"
        @click.prevent="submit"
      >
        Save
      </button>
    </div>
  </form>
</template>

<script>
import CustomInput from "@/components/form/CustomInput";
import { UserService } from "@/services/UserService";

const errors = {
  empty: "This field can't be empty.",
  same: "Your new password can't be the same as your current password.",
  tooShort: "The new password is too short.",
  noMatch: "The new passwords don't match.",
};

export default {
  components: {
    CustomInput,
  },

  data() {
    return {
      current: {
        errors: [],
        value: "",
      },
      password1: {
        errors: [],
        value: "",
      },
      password2: {
        errors: [],
        value: "",
      },
    };
  },

  methods: {
    validate() {
      this.current.errors = [];
      this.password1.errors = [];
      this.password2.errors = [];

      // Empty fields
      if (!this.current.value) {
        this.current.errors.push(errors.empty);
      }
      if (!this.password1.value) {
        this.password1.errors.push(errors.empty);
      }
      if (!this.password2.value) {
        this.password2.errors.push(errors.empty);
      }

      if (this.password1.value) {
        // New password is same as the old password
        if (this.current.value === this.password1.value) {
          this.password1.errors.push(errors.same);
        }

        // New password is too short
        if (this.password1.value.length < 8) {
          this.password1.errors.push(errors.tooShort);
        }

        // New passwords don't match
        if (
          this.password2.value &&
          this.password1.value !== this.password2.value
        ) {
          this.password2.errors.push(errors.noMatch);
        }
      }

      return (
        this.current.errors.length === 0 &&
        this.password1.errors.length === 0 &&
        this.password2.errors.length === 0
      );
    },

    onEdit(fieldName) {
      let field = this[fieldName];
      field.edited = true;
      field.maxLength = Math.max(field.maxTyped, field.value.length);
    },

    async submit() {
      if (!this.validate()) {
        return;
      }

      let { ok, content } = await UserService.changePassword({
        current: this.current.value,
        password1: this.password1.value,
        password2: this.password2.value,
      });

      if (!ok) {
        for (let error of content.errors) {
          this.$store.commit("addNotification", {
            message: error,
            status: "error",
          });
        }

        return;
      }

      this.$store.commit("addNotification", {
        message: "Your password was changed successfully.",
        status: "success",
      });

      this.$emit("success");
    },
  },
};
</script>

<style lang="scss" scoped>
.password-form {
  width: 100%;
}

.form-buttons {
  justify-content: space-between;
}
</style>
