<template>
  <FixedWidthContainer>
    <h2>Users</h2>

    <table v-if="!loading">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Groups</th>
          <th class="user-log-in">Last log in</th>
          <th class="user-date-joined">Date joined</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(user, index) in users" :key="index">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}<span v-if="user.isStaff">*</span></td>
          <td>{{ user.email }}</td>
          <td>{{ formatGroups(user.groups) }}</td>
          <td class="user-log-in">{{ formatDateTime(user.lastLogin) }}</td>
          <td class="user-date-joined">{{ formatDate(user.dateJoined) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading...</p>
  </FixedWidthContainer>
</template>

<script>
import { mapState } from "vuex";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import { formatDate, formatDateTime } from "@/date";
import { ManageUserService } from "@/services/manage/ManageUserService";

export default {
  components: {
    FixedWidthContainer,
  },

  computed: {
    ...mapState(["loading"]),
  },

  data() {
    return {
      users: [],
    };
  },

  async created() {
    this.$store.commit("setBreadcrumbs", [
      { label: "Manage", to: { name: "manage" } },
      { label: "Users", to: { name: "users" } },
    ]);

    this.$store.commit("setLoading", true);
    this.users = await ManageUserService.listUsers();
    this.$store.commit("setLoading", false);
  },

  methods: {
    formatDate: formatDate,
    formatDateTime: formatDateTime,

    formatGroups(groups) {
      return groups
        .slice()
        .sort((a, b) => a.localeCompare(b))
        .join(", ");
    },
  },
};
</script>

<style scoped lang="scss">
.user-log-in,
.user-date-joined {
  white-space: nowrap;
}
</style>
