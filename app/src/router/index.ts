/*
 * HealthCam: Protective Equipment Detection
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";
import VueRouter from "vue-router";
import DashboardView from "@/views/DashboardView.vue";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "DashboardView",
        component: DashboardView,
    },
    {
        path: "/activity-log",
        name: "ActivityLogView.vue",
        component: () => import(/* webpackChunkName: "activity-log" */ "@/views/ActivityLogView.vue"),
    },
    {
        path: "/about",
        name: "AboutView",
        component: () => import(/* webpackChunkName: "about" */ "@/views/AboutView.vue"),
    },
];

// noinspection TypeScriptUnresolvedVariable
const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
