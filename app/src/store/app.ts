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
    CameraState,
    IActivity,
    IActivityHistory,
    ICamera,
} from "@/store/models";

function cameraStateFromPingTimestamp(timestamp: Date): CameraState {
    return new Date().getTime() - timestamp.getTime() > 60 * 1000
        ? "offline" : "online";
}

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
        compliant: [],
        violation: [],
        override: [],
    };

    get hasViolation() {
        return this.activities.some(a => a.type === "violation");
    }

    @Mutation
    setActivities(payload: { activities: IActivity[] }) {
        this.activities = payload.activities;
        this.activities.sort((lhs, rhs) => rhs.timestamp.getTime() - lhs.timestamp.getTime());
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
    async doRateActivity(payload: { activityId: string; rating: number }) {
        await axios.post(`${process.env.VUE_APP_API_URL}/rate`, {
            "activity_id": payload.activityId,
            rating: payload.rating,
        });

        this.deleteActivity({activityId: payload.activityId});
    }

    @Action({rawError: true})
    async doFetchStats() {
        const result = await axios.get(`${process.env.VUE_APP_API_URL}/stats`);
        this.setStats({
            cameras: result.data.cameras.map((c: any): ICamera => ({
                id: c.id,
                name: c.deviceName,
                state: cameraStateFromPingTimestamp(new Date(c.pingedOn)),
                compliantCount: c.compliantCount,
                violationCount: c.violationCount,
                overrideCount: c.overrideCount,
            })),
            activityHistory: result.data.activityHistory,
        });
    }
}
