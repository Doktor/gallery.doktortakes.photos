import UserDetailPage from "@/pages/user/UserDetailPage";
import ChangePasswordPage from "@/pages/user/ChangePasswordPage";

import LogInPage from "@/pages/user/LogInPage";
import LogOutPage from "@/pages/user/LogOutPage";

export const userRoutes = [
  {
    path: "/users/:slug/",
    name: "user",
    component: UserDetailPage,
    meta: {
      title: false,
    },
  },
  {
    path: "/users/:slug/password/",
    name: "changePassword",
    component: ChangePasswordPage,
    meta: {
      title: "Change your password",
    },
  },

  {
    path: "/log-in/",
    name: "logIn",
    component: LogInPage,
    meta: {
      title: "Log in",
    },
  },
  {
    path: "/log-out/",
    name: "logOut",
    component: LogOutPage,
    meta: {
      title: "Log out",
    },
  },
];
