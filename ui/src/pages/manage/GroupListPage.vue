<template>
  <FixedWidthContainer>
    <router-link :to="{ name: 'manage' }">Back to editor</router-link>

    <h2>Groups</h2>

    <table v-if="!loading">
      <thead>
        <tr>
          <th>ID</th>
          <th class="group-name">Name</th>
          <th>Users</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(group, index) in groups" :key="index">
          <td>{{ group.id }}</td>
          <td class="group-name">{{ group.name }}</td>
          <td>{{ formatUsers(group.users) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading...</p>
  </FixedWidthContainer>
</template>

<script>
import { mapState } from "vuex";
import FixedWidthContainer from "../../components/FixedWidthContainer.vue";
import { ManageUserService } from "../../services/manage/ManageUserService";

export default {
  components: {
    FixedWidthContainer,
  },

  computed: {
    ...mapState(["loading"]),
  },

  data() {
    return {
      groups: [],
    };
  },

  async created() {
    this.$store.commit("setLoading", true);
    this.groups = await ManageUserService.listGroups();
    this.$store.commit("setLoading", false);
  },

  methods: {
    formatUsers(users) {
      return users
        .slice()
        .sort((a, b) => a.localeCompare(b))
        .join(", ");
    },
  },
};
</script>

<style scoped lang="scss">
.group-name {
  white-space: nowrap;
}
</style>
