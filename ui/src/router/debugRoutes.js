import DebugNotificationsPage from "@/pages/debug/DebugNotificationsPage";

export const debugRoutes = [
  {
    path: "/debug/notifications",
    name: "debugNotifications",
    component: DebugNotificationsPage,
    meta: {
      staff: true,
      title: "Debug | Notifications",
    },
  },
];
