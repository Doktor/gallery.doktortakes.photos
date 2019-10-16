<template>
  <form>
    <fieldset>
      <PasswordFormField
          :name="'Current'"
          v-model="current.value"
          @input="onEdit('current')"
          :errors="current.errors"
      />
    </fieldset>

    <fieldset>
      <legend>Set your password</legend>

      <PasswordFormField
          :name="'Password'"
          v-model="password1.value"
          @input="onEdit('password1')"
          :errors="password1.errors"
          :help-text="'Your password must contain at least 8 characters.'"
      />

      <PasswordFormField
          :name="'Repeat'"
          v-model="password2.value"
          @input="onEdit('password2')"
          :errors="password2.errors"
      />
    </fieldset>

    <div class="form-buttons">
      <router-link
          class="form-button form-button-cancel"
          :to="{name: 'user'}"
      >
        Cancel
      </router-link>

      <button
          class="form-button form-button-save"
          type="submit"
          @click.prevent="submit"
      >
        Save
      </button>
    </div>
  </form>
</template>

<script>
  import PasswordFormField from "./PasswordFormField.vue";


  const errors = {
    empty: "This field can't be empty.",
    same: "Your new password can't be the same as your current password.",
    tooShort: "The new password is too short.",
    noMatch: "The new passwords don't match."
  };


  export default {
    components: {
      PasswordFormField,
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
      }
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
          if (this.password1.value.length < 8
              && (force || this.password1.maxTyped >= 8)) {
            this.password1.errors.push(errors.tooShort);
          }

          // New passwords don't match
          if (this.password2.value
              && this.password1.value !== this.password2.value) {
            this.password2.errors.push(errors.noMatch);
          }
        }

        return this.current.errors.length === 0
            && this.password1.errors.length === 0
            && this.password2.errors.length === 0;
      },

      onEdit(fieldName) {
        let field = this[fieldName];
        field.edited = true;
        field.maxLength = Math.max(field.maxTyped, field.value.length);

        this.validate();
      },

      submit() {
        if (this.validate(true)) {
          this.$store.dispatch('changePassword', {
            current: this.current.value,
            password1: this.password1.value,
            password2: this.password2.value,
          });
        }
      },
    }
  }
</script>

<style lang="scss" scoped>
  $text: rgb(220, 220, 220);
  $blue: rgb(0, 120, 255);

  form {
    width: 50%;
    margin: 0 auto;
  }

  .form-buttons {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    width: 100%;
  }

  .form-button {
    display: block;

    width: 110px;
    padding: 8px 0;
    border: 0;
    border-radius: 4px;

    background-color: $text;
    color: rgb(20, 20, 20);

    text-align: center;
    text-decoration: none;

    &:hover {
      background-color: lighten($text, 15%);
      text-decoration: none;
    }

    &, &:hover {
      transition: background-color 0.3s;
    }
  }

  .form-button-cancel { }

  .form-button-save {
    background-color: $blue;
    color: white;

    &:hover {
      background-color: lighten($blue, 15%);
    }
  }
</style>
