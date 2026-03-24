import { createRouter, createWebHistory } from "vue-router";

import { useStore } from "@/store";

import { publicRoutes } from "./publicRoutes";
import { userRoutes } from "./userRoutes";
import { manageRoutes } from "./manageRoutes";
import { debugRoutes } from "./debugRoutes";

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
  const store = useStore();

  if (to.matched.some((record) => record.meta.staff)) {
    let user = store.user;

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
  const store = useStore();

  if (from.name !== to.name) {
    store.setBreadcrumbs([]);
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

    store.showNavigation = record.meta?.showNavigation ?? true;

    // Document title
    let title = record.meta.title;

    if (typeof title === "string") {
      store.setTitle(title);
    }
  }
});

export { router };
