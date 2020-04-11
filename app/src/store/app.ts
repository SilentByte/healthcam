/*
 * HealthCam: Protective Equipment Detection
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import {
    VuexModule,
    Module,
} from "vuex-module-decorators";

import store from "@/store";

import {
    IActivity,
    IActivityHistory,
    ICamera,
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
            camera: "ICU Entrance North",
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

    activityHistory: IActivityHistory = {
        detections: [10, 15, 16, 18, 12, 8, 4, 6, 4, 8, 11, 12],
        rates: [5, 4, 2, 0, -2, -3, -8, -2, 4, 10, 8, 9],
    };

    cameras: ICamera[] = [
        {
            id: "icu-north",
            name: "ICU Entrance North",
            state: "online",
            compliantCount: 0,
            violationCount: 0,
            overrideCount: 0,
        },
        {
            id: "er-east",
            name: "ER East",
            state: "offline",
            compliantCount: 0,
            violationCount: 0,
            overrideCount: 0,
        },
    ];

    get hasViolation() {
        return this.activities.some(a => a.type === "violation");
    }
}
