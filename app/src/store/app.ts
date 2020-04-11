/*
 * SmartCam
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import {
    VuexModule,
    Module,
} from "vuex-module-decorators";

import store from "@/store";

import {
    IActivity,
} from "@/store/models";

@Module({
    store,
    dynamic: true,
    namespaced: true,
    name: "app",
})
export class AppModule extends VuexModule {
    activities: IActivity[] = [
        {
            id: "1",
            type: "compliant",
            timestamp: new Date(),
            camera: "ICU Entrance North",
            photoUrl: "https://picsum.photos/seed/1/500/500",
        },
        {
            id: "2",
            type: "violation",
            timestamp: new Date(),
            camera: "ICU Entrance West",
            photoUrl: "https://picsum.photos/seed/2/500/500",
        },
        {
            id: "3",
            type: "override",
            timestamp: new Date(),
            camera: "ER East",
            photoUrl: "https://picsum.photos/seed/3/500/500",
        },
    ];

    get hasViolation() {
        return this.activities.some(a => a.type === "violation");
    }
}
