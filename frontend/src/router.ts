import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";

import ContactDetailPage from "./views/ContactDetailPage.vue";
import ContactListPage from "./views/ContactListPage.vue";

const routes: RouteRecordRaw[] = [
  { path: "/", redirect: { name: "contact-list" } },
  { path: "/contacts", component: ContactListPage, name: "contact-list" },
  { path: "/contacts/:id", component: ContactDetailPage, name: "contact-detail" }
];

const router = createRouter({
  history: createWebHistory("/app"),
  routes
});

export default router;
