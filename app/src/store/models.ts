/*
 * SmartCam
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export type ActivityType = "compliant" | "violation" | "override";
export type CameraState = "online" | "offline";

export interface IActivity {
    id: string;
    type: ActivityType;
    timestamp: Date;
    camera: string;
    photoUrl: string;
}

export interface ICamera {
    id: string;
    name: string;
    state: CameraState
    compliantCount: number;
    violationCount: number;
    overrideCount: number;
}
