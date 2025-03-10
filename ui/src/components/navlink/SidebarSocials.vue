<template>
  <SidebarSection>
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
  </SidebarSection>
</template>

<script>
import FontAwesomeCircleIcon from "./FontAwesomeCircleIcon";
import NavlinkSocial from "./NavlinkSocial";
import SidebarSection from "./SidebarSection";

export default {
  name: "SidebarSocials",
  components: {
    SidebarSection,
    FontAwesomeCircleIcon,
    NavlinkSocial,
  },
};
</script>
