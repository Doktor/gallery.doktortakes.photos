<template>
  <form class="form--1-column form--small">
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
        edited: false,
        maxTyped: 0,

        errors: [],
        value: "",
      },
      password1: {
        edited: false,
        maxTyped: 0,

        errors: [],
        value: "",
      },
      password2: {
        edited: false,
        maxTyped: 0,

        errors: [],
        value: "",
      },
    };
  },

  methods: {
    validate(force = false) {
      this.current.errors = [];
      this.password1.errors = [];
      this.password2.errors = [];

      // Empty fields
      if ((force || this.current.edited) && !this.current.value) {
        this.current.errors.push(errors.empty);
      }
      if ((force || this.password1.edited) && !this.password1.value) {
        this.password1.errors.push(errors.empty);
      }
      if ((force || this.password2.edited) && !this.password2.value) {
        this.password2.errors.push(errors.empty);
      }

      if (this.password1.value) {
        // New password is same as the old password
        if (this.current.value === this.password1.value) {
          this.password1.errors.push(errors.same);
        }

        // New password is too short
        if (
          this.password1.value.length < 8 &&
          (force || this.password1.maxTyped >= 8)
        ) {
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

      this.validate();
    },

    submit() {
      if (this.validate(true)) {
        this.$store.dispatch("changePassword", {
          current: this.current.value,
          password1: this.password1.value,
          password2: this.password2.value,
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
form {
  width: 50%;
  margin: 0 auto;
}

.form-buttons {
  justify-content: space-between;
}
</style>
