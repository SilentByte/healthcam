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

export interface ICameraStats {
    id: string;
    name: string;
    state: CameraState
    compliantCount: number;
    violationCount: number;
    overrideCount: number;
}

export interface IStats {
    cameras: ICameraStats[];
    compliantCount: number;
    violationCount: number;
    overrideCount: number;
}
