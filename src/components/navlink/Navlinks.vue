<template>
  <nav v-if="showNav" class="nav">
    <ul class="nav-items" :class="{ 'nav-items-index': isIndex }">
      <template v-if="showLogo">
        <NavlinksLogo />
        <NavlinkDivider v-if="showDividers" />
      </template>

      <!-- Main links -->
      <Navlink title="Featured" route="featured" />

      <Navlink v-if="isIndex" title="Albums" display="Photos" route="albums" />
      <NavlinkMenu v-else title="Photos">
        <Navlink title="Archive" display="Archive" route="albums" />
        <Navlink
          v-if="user.status !== 'anonymous'"
          title="Your albums"
          :to="{ name: 'user', params: { slug: user.name } }"
        />
        <Navlink title="Tags" route="tags" />
        <Navlink title="Search" route="search" />
      </NavlinkMenu>

      <Navlink title="About" route="about" />

      <!-- Social media links -->
      <template v-if="!userIsStaff && !isIndex">
        <NavlinkDivider v-if="showDividers" />

        <!-- Twitter -->
        <NavlinkSocial
          href="https://twitter.com/DoktorTheHusky"
          title="Twitter"
        >
          <span class="fa-stack">
            <i class="fab fa-twitter"></i>
          </span>
        </NavlinkSocial>

        <!-- Telegram -->
        <NavlinkSocial href="https://t.me/DoktorTakesPhotos" title="Telegram">
          <i class="fab fa-telegram"></i>
        </NavlinkSocial>

        <!-- Website -->
        <NavlinkSocial href="https://doktorthehusky.com" title="Website">
          <i class="fas fa-globe-americas"></i>
        </NavlinkSocial>
      </template>

      <!-- Content management -->
      <NavlinkDivider v-if="showDividers" />
      <template v-if="userIsStaff">
        <li class="nav-item">
          <a class="nav-item-link" href="/admin/">Admin</a>
        </li>
        <Navlink title="Edit" route="editorIndex" />
      </template>

      <!-- User management -->
      <template v-if="isAuthenticated">
        <Navlink
          class="nav-item-profile"
          title="Profile"
          :to="{ name: 'user', params: { slug: user.name } }"
        />
        <Navlink class="nav-item-log-out" title="Log out" route="logOut" />
      </template>
      <Navlink
        v-else-if="!isIndex && !isAuthenticated"
        title="Log in"
        route="logIn"
      />
    </ul>
  </nav>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import Navlink from "@/components/navlink/Navlink.vue";
import NavlinkDivider from "@/components/navlink/NavlinkDivider.vue";
import NavlinkSocial from "@/components/navlink/NavlinkSocial.vue";
import NavlinksLogo from "@/components/navlink/NavlinksLogo.vue";
import NavlinkMenu from "@/components/navlink/NavlinkMenu.vue";

export default {
  components: {
    NavlinkMenu,
    NavlinksLogo,
    NavlinkSocial,
    NavlinkDivider,
    Navlink,
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
    ...mapState(["showNav", "user"]),

    isIndex() {
      return this.$route.name === "index";
    },

    userIsStaff() {
      return this.user.status === "staff" || this.user.status === "superuser";
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
};
</script>

<style lang="scss">
// Base font size
$nav-font-size: 1.5rem;
$nav-font-size-index: $nav-font-size * 1.25;
$logo-size: $nav-font-size * 1.5;

// Color of nav items (on the index page)
$nav-item-color: $text-color;

// Spacing between nav items
$nav-item-spacing: 1.7rem;

.nav-items .logo {
  @include logo-font();

  color: $nav-item-color;
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
  padding-bottom: 0.5rem;
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

  @include headings-font();
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

.nav-item-link {
  color: $nav-item-color;

  .nav-item-profile & {
    color: $text-blue;
  }

  .nav-item-log-out & {
    color: $text-error;
  }

  .nav-items-index & {
    color: $background-color;
    line-height: 1;

    &:hover {
      text-decoration: underline;
    }

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

  color: $background-color;
  background-color: $text-color;

  .nav-items-index & {
    &:hover {
      text-decoration: underline;
    }

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
</style>
