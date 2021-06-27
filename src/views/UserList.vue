<template>
  <FixedWidthContainer>
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
          <td>{{ user.username }}<span v-if="user.is_staff">*</span></td>
          <td>{{ user.email }}</td>
          <td>{{ formatGroups(user.groups) }}
          <td class="user-log-in">{{ formatDateTime(user.last_login) }}</td>
          <td class="user-date-joined">{{ formatDate(user.date_joined) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading...</p>
  </FixedWidthContainer>
</template>

<script>
import {mapState} from 'vuex';
import FixedWidthContainer from "@/components/FixedWidthContainer";
import {formatDate, formatDateTime} from "@/date.js";


export default {
  components: {
    FixedWidthContainer,
  },

  computed: {
    ...mapState([
      'loading',
      'users',
    ]),
  },

  created() {
    this.$store.dispatch('getUsers');
  },

  methods: {
    formatDate: formatDate,
    formatDateTime: formatDateTime,

    formatGroups(groups) {
      return groups.slice().sort((a, b) => a.localeCompare(b)).join(', ');
    },
  },
}
</script>

<style scoped>
table {
  margin: 0 auto;
}

thead {
  background-color: rgb(60, 60, 60);
  text-align: center;
}

th, td {
  padding: 4px 8px;
}

.user-log-in, .user-date-joined {
  white-space: nowrap;
}

tr:nth-child(even) {
  background-color: rgb(40, 40, 40);
}
</style>
