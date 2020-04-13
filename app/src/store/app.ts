/*
 * HealthCam: Protective Equipment Detection
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import {
    VuexModule,
    Module,
    Mutation,
    Action,
} from "vuex-module-decorators";

import axios from "axios";
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
    activities: IActivity[] = [];

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

    @Mutation
    setActivities(payload: { activities: IActivity[] }) {
        this.activities = payload.activities;
    }

    @Mutation
    deleteActivity(payload: { activityId: string }) {
        this.activities = this.activities.filter(a => a.id !== payload.activityId);
    }

    @Action({rawError: true})
    async doFetchActivities() {
        const result = await axios.get(`${process.env.VUE_APP_API_URL}/activities`);

        const activities = result.data.map((a: any): IActivity => ({
            id: a.id,
            type: a.type,
            timestamp: new Date(a.timestamp),
            camera: a.camera,
            photoUrl: a.photoUrl,
            minConfidence: a.minConfidence,
            peopleInFrame: a.peopleInFrame,
        }));

        this.setActivities({activities});
    }

    @Action({rawError: true})
    async doConfirmActivity(payload: { activityId: string }) {
        // TODO: Implement API call.
        await new Promise(function(resolve) {
            setTimeout(resolve.bind(null, () => null), 1000);
        });

        this.deleteActivity({activityId: payload.activityId});
    }
}
