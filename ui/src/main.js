import { createApp } from "vue";

import Base from "./pages/public/Base";
import { router } from "./router";
import { store } from "./store";

import "./styles/main.scss";
import "./styles/forms.scss";

const app = createApp(Base);

store.commit("setApiTokenFromLocalStorage");
await store.dispatch("getUser");

app.use(router);
app.use(store);

app.mount("#app");
