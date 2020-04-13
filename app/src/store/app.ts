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

    cameras: ICamera[] = [];

    activityHistory: IActivityHistory = {
        detections: [],
        rates: [],
    };

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

    @Mutation
    setStats(payload: { cameras: ICamera[]; activityHistory: IActivityHistory }) {
        this.cameras = payload.cameras;
        this.activityHistory = payload.activityHistory;
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
        await axios.post(`${process.env.VUE_APP_API_URL}/confirm`, {
            "activity_id": payload.activityId,
        });

        this.deleteActivity({activityId: payload.activityId});
    }

    @Action({rawError: true})
    async doFetchStats() {
        const result = await axios.get(`${process.env.VUE_APP_API_URL}/stats`);
        this.setStats({
            cameras: result.data.cameras,
            activityHistory: result.data.activityHistory,
        });
    }
}
