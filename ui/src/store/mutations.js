export const titleTemplate = "{0} | Doktor Takes Photos";
export const editorTitleTemplate = "Editing {0} | Doktor Takes Photos";

export const mutations = {
  setApiTokenFromLocalStorage(state) {
    state.token = localStorage.getItem("token");
  },

  setApiToken(state, token) {
    state.token = token;
    localStorage.setItem("token", token);
  },

  logOut(state) {
    state.token = null;
    localStorage.removeItem("token");

    state.user = { status: "anonymous" };
  },

  addNotification(state, { message, status = "default" }) {
    state.notificationId += 1;

    let notification = { id: state.notificationId, message, status };
    state.notifications.push(notification);

    return notification.id;
  },

  addTimedNotification(state, { message, status = "default", hideAfter = 0 }) {
    let id = this.commit("addNotification", { message, status });

    if (hideAfter > 0) {
      setTimeout(() => this.commit("removeNotification", id), hideAfter);
    }
  },

  removeNotification(state, id) {
    let index = state.notifications.findIndex((n) => n.id === id);
    state.notifications.splice(index, 1);
  },

  setUser(state, user) {
    state.user = user;
  },

  setLoading(state, loading) {
    loading ? (state.loading += 1) : (state.loading -= 1);
  },
};
