export const getters = {
  isAuthenticated(state) {
    return state.token !== null;
  },
  isStaff(state) {
    return state.user.status === "staff" || state.user.status === "superuser";
  },
};
