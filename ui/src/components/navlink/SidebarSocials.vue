<template>
  <li class="nav-section">
    <h2>Links</h2>

    <div class="nav-socials">
      <!-- Twitter -->
      <NavlinkSocial href="https://twitter.com/DoktorTheHusky" title="Twitter">
        <FontAwesomeCircleIcon iconClass="fab fa-twitter" />
      </NavlinkSocial>

      <!-- Telegram -->
      <NavlinkSocial href="https://t.me/DoktorTakesPhotos" title="Telegram">
        <i class="fab fa-telegram"></i>
      </NavlinkSocial>

      <!-- Website -->
      <NavlinkSocial href="https://doktorthehusky.com" title="Website">
        <i class="fas fa-globe-americas"></i>
      </NavlinkSocial>
    </div>
  </li>
</template>

<script>
import FontAwesomeCircleIcon from "./FontAwesomeCircleIcon";
import NavlinkSocial from "./NavlinkSocial";

export default {
  name: "SidebarSocials",
  components: {
    FontAwesomeCircleIcon,
    NavlinkSocial,
  },
};
</script>

<style lang="scss">
.nav-socials {
  display: flex;
  flex-direction: row;
  gap: 16px;
}
</style>
