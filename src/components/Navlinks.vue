<template>
  <nav class="nav">
  <ul class="nav-items" :class="{'nav-items-index': isIndex}">
    <template v-if="showLogo">
      <li class="nav-item">
        <h1 class="logo">
          <router-link
              class="nav-item-link"
              title="Doktor Takes Photos"
              :to="{name: 'index'}"
          >
            Doktor Takes Photos
          </router-link>
        </h1>
      </li>
      <li v-if="showDividers" class="nav-divider"></li>
    </template>

    <!-- Main links -->
    <li class="nav-item">
      <router-link
          class="nav-item-link"
          title="About"
          :to="{name: 'about'}"
      >
        About
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
          class="nav-item-link"
          title="Featured"
          :to="{name: 'featured'}"
      >
        Featured
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
          class="nav-item-link"
          title="Albums"
          :to="{name: 'albums'}"
      >
        Photos
      </router-link>
    </li>

    <!-- Social media links -->
    <template v-if="!userIsStaff && !isIndex">
      <li v-if="showDividers" class="nav-divider"></li>

      <!-- Twitter -->
      <li class="nav-item">
        <a class="nav-item-link nav-item-fa-wrapper"
           href="https://twitter.com/DoktorTheHusky"
           target="blank"
           rel="noopener noreferrer"
           title="Twitter">
          <span class="fa-stack">
            <i class="fab fa-twitter"></i>
          </span>
        </a>
      </li>

      <!-- Telegram -->
      <li class="nav-item">
        <a class="nav-item-link nav-item-fa-wrapper"
           href="https://t.me/DoktorTakesPhotos"
           target="blank"
           rel="noopener noreferrer"
           title="Telegram">
          <i class="fab fa-telegram"></i>
        </a>
      </li>

      <!-- Website -->
      <li class="nav-item">
        <a class="nav-item-link nav-item-fa-wrapper"
           href="https://doktorthehusky.com"
           target="blank"
           rel="noopener noreferrer"
           title="Website">
          <i class="fas fa-globe-americas"></i>
        </a>
      </li>
    </template>

    <!-- Content management -->
    <li v-if="showDividers" class="nav-divider"></li>
    <template v-if="userIsStaff">
      <li class="nav-item">
        <a class="nav-item-link" href="/admin/">Admin</a>
      </li>
      <li class="nav-item">
        <router-link
            class="nav-item-link"
            :to="{name: 'editorIndex'}"
        >
          Edit
        </router-link>
      </li>
    </template>

    <!-- User management -->
    <template v-if="isAuthenticated">
      <li class="nav-item">
        <router-link
            class="nav-item-link nav-item-link-profile"
            :to="{name: 'user', params: {slug: user.name}}"
        >
          {{ user.name }}
        </router-link>
      </li>
      <li class="nav-item">
        <router-link
            class="nav-item-link nav-item-link-log-out"
            :to="{name: 'logOut'}"
        >
          Log out
        </router-link>
      </li>
    </template>
    <li v-else-if="!isIndex && !isAuthenticated" class="nav-item">
      <router-link class="nav-item-link" :to="{name: 'logIn'}">
        Log in
      </router-link>
    </li>
  </ul>
  </nav>
</template>

<script>
  import {mapGetters, mapState} from 'vuex';


  export default {
    computed: {
      ...mapGetters([
        'isAuthenticated',
      ]),
      ...mapState([
        'user',
      ]),

      isIndex() {
        return this.$route.name === 'index';
      },

      userIsStaff() {
        return this.user.status === 'staff' || this.user.status === 'superuser';
      },
    },

    props: {
      showDividers: {
        type: Boolean,
        default: true,
      },
      showLogo: {
        type: Boolean,
        default: false,
      },
    },
  }
</script>

<style lang="scss" scoped>
  // Base font size
  $nav-font-size: 1.5rem;
  $nav-font-size-index: $nav-font-size * 1.25;
  $logo-size: $nav-font-size * 1.5;

  // Color of nav items (on the index page)
  $nav-item-color: white;

  // Color of nav dividers (on non-index pages)
  $nav-divider-color: rgb(120, 120, 120);

  // Spacing between nav items
  $nav-item-spacing: 1.7rem;

  .logo {
    font-size: $logo-size;
    line-height: 1;
    text-align: center;
    text-transform: capitalize;

    padding: 0;
    margin: 0 0 1rem 0;

    @media (min-width: 901px) {
      font-size: $logo-size * 1.15;
      margin: 0;
    }
  }

  .nav {
    padding-bottom: 1.5rem;
    margin-top: -0.5rem;
  }

  .nav-index {
    padding: 0;
    margin: 0;
  }

  .nav-items {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;

    @include primary-font();
    font-size: $nav-font-size;
    text-transform: lowercase;

    list-style: none;
    padding: 0;
    margin: 0;
    margin-bottom: -1rem;

    @media (min-width: 901px) {
      margin: 0;
    }
  }

  .nav-items-index {
    justify-content: flex-start;
  }

  .nav-item {
    display: flex;
    justify-content: center;
    align-items: center;

    margin: 0 ($nav-item-spacing / 3);
    margin-bottom: 1rem;

    @media (min-width: 901px) {
      margin: 0 ($nav-item-spacing / 2);

      // Vertical alignment
      line-height: $logo-size * 1.15;

      .nav-items-index & {
        &:first-child {
          margin-left: 0;
        }

        &:last-child {
          margin-right: 0;
        }
      }
    }
  }

  // Change color of items on hover
  @mixin nav-item-hover($property) {
    #{$property}: $nav-item-color;

    &:hover {
      #{$property}: $text;
    }

    &, &:hover {
      text-decoration: none;
      transition: #{$property} 0.25s;
    }
  }

  .nav-item-link {
    color: $text;

    &-profile {
      color: $blue;
    }

    &-log-out {
      color: red;
    }

    .nav-items-index & {
      @include nav-item-hover(color);

      color: white;
      line-height: 1;

      @media (min-width: 901px) {
        font-size: $nav-font-size-index;
      }
    }
  }

  // Displays a Font Awesome icon in a circle
  // The icon element should be the only child element of a container element
  // with this class.
  .fa-stack {
    display: flex;
    justify-content: center;
    align-items: center;

    // Background: circle
    width: 24px;
    height: 24px;
    border-radius: 100%;

    color: rgb(20, 20, 20);
    background-color: $text;

    .nav-items-index & {
      @include nav-item-hover(background-color);

      @media (min-width: 901px) {
        width: $nav-font-size-index;
        height: $nav-font-size-index;
      }
    }

    // Foreground: icon
    i {
      font-size: 55%;
    }
  }

  .nav-item-fa-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;

    &:hover {
      text-decoration: none;
    }
  }

  .nav-divider {
    color: $nav-divider-color;
    margin: 0 ($nav-item-spacing / 3) !important;

    &::before {
      content: "\00b7";  // Center dot
    }
  }
</style>
