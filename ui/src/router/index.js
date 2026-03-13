import { createRouter, createWebHistory } from "vue-router";

import { store } from "@/store";

import { publicRoutes } from "./publicRoutes";
import { userRoutes } from "./userRoutes";
import { manageRoutes } from "./manageRoutes";
import { debugRoutes } from "./debugRoutes";

export const baseTitle = "Doktor Takes Photos";

const routes = [
  ...publicRoutes,
  ...userRoutes,
  ...manageRoutes,
  ...debugRoutes,
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  strict: true,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.staff)) {
    let user = store.state.user;

    if (user.status === "staff" || user.status === "superuser") {
      next();
    } else {
      next({
        name: "logIn",
        query: {
          redirect: to.fullPath,
        },
      });
    }
  } else {
    next();
  }
});

router.afterEach((to, from) => {
  if (to.name !== from.name) {
    window.scrollTo(0, 0);
  }

  for (let record of to.matched) {
    // <body>
    let body = record.meta.body;

    if (body === undefined) {
      document.body.className = "";
    } else {
      document.body.className = body;
    }

    store.state.showNavigation = record.meta?.showNavigation ?? true;

    // Document title
    let title = record.meta.title;

    if (title === false) {
      // Don't change the title
    } else if (title !== undefined) {
      document.title = title + " | " + baseTitle;
    } else {
      document.title = baseTitle;
    }
  }
});

export { router };
