<template>
  <ul>
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
    <template v-if="!userIsStaff">
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
    <template v-if="user.status !== 'anonymous'">
      <li class="nav-item">
        <router-link
            class="nav-item-link nav-item-link-profile"
            :to="{name: 'user', params: {slug: user.name}}"
        >
          {{ user.name }}
        </router-link>
      </li>
      <li class="nav-item">
        <a class="nav-item-link nav-item-link-log-out" href="/log-out/">
          Log out
        </a>
      </li>
    </template>
    <li v-else class="nav-item">
      <a class="nav-item-link" href="/log-in/">
        Log in
      </a>
    </li>
  </ul>
</template>

<script>
  import {mapState} from 'vuex';


  export default {
    computed: {
      ...mapState([
        'user',
      ]),

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
