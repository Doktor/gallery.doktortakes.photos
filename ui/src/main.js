import { createApp } from "vue";
import { createPinia } from "pinia";

import Base from "./pages/public/Base";
import { router } from "./router";
import { useStore } from "./store";

import "vite/modulepreload-polyfill";
import "normalize.css";

import "./styles/main.scss";
import "./styles/forms.scss";

const app = createApp(Base);

app.use(createPinia());

const store = useStore();
store.setApiTokenFromLocalStorage();
await store.getUser();

app.use(router);

app.mount("#app");
