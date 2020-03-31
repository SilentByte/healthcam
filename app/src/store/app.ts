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
    ICamera,
    PerimeterStatus,
} from "@/store/models";

@Module({
    store,
    dynamic: true,
    namespaced: true,
    name: "app",
})
export class AppModule extends VuexModule {
    perimeterStatus: PerimeterStatus = "clear";

    cameras: ICamera[] = [
        {
            id: "1",
            name: "Cam01",
            location: [0, 0],
            latestPhotoUrl: "https://picsum.photos/seed/1/500/500",
            latestPhotoDateTime: new Date(),
        },
        {
            id: "2",
            name: "Cam02",
            location: [0, 0],
            latestPhotoUrl: "https://picsum.photos/seed/2/500/500",
            latestPhotoDateTime: new Date(),
        },
        {
            id: "3",
            name: "Cam03",
            location: [0, 0],
            latestPhotoUrl: "https://picsum.photos/seed/3/500/500",
            latestPhotoDateTime: new Date(),
        },
    ];
}
