import { defineStore } from "pinia";
import { UserService } from "@/services/UserService";

export const useStore = defineStore("main", {
  state: () => ({
    token: null,
    showNavigation: true,
    breadcrumbs: [],
    title: null,

    user: {},
    notifications: [],
    notificationId: 0,

    loading: 0,
  }),

  getters: {
    isAuthenticated(state) {
      return state.token !== null;
    },
    isStaff(state) {
      return state.user.status === "staff" || state.user.status === "superuser";
    },
  },

  actions: {
    setApiTokenFromLocalStorage() {
      this.token = localStorage.getItem("token");
    },

    setApiToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
    },

    logOut() {
      this.token = null;
      localStorage.removeItem("token");

      this.user = { status: "anonymous" };
    },

    addNotification({ message, status = "default" }) {
      this.notificationId += 1;

      let notification = { id: this.notificationId, message, status };
      this.notifications.push(notification);

      return notification.id;
    },

    addTimedNotification({ message, status = "default", hideAfter = 0 }) {
      let id = this.addNotification({ message, status });

      if (hideAfter > 0) {
        setTimeout(() => this.removeNotification(id), hideAfter);
      }
    },

    removeNotification(id) {
      let index = this.notifications.findIndex((n) => n.id === id);
      this.notifications.splice(index, 1);
    },

    setUser(user) {
      this.user = user;
    },

    setLoading(loading) {
      loading ? (this.loading += 1) : (this.loading -= 1);
    },

    setBreadcrumbs(items) {
      this.breadcrumbs = items;
    },

    setTitle(title) {
      const baseTitle = "Doktor Takes Photos";

      if (title) {
        document.title = title + " | " + baseTitle;
        this.title = title;
      } else {
        document.title = baseTitle;
        this.title = null;
      }
    },

    async ensureCsrfToken() {
      await UserService.ensureCsrfToken();
    },

    async authenticate({ username, password }) {
      return await UserService.authenticate(username, password);
    },

    async getUser() {
      let content = await UserService.getUser();
      this.setUser(content);
    },
  },
});
