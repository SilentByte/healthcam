/*
 * HealthCam: Protective Equipment Detection
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
    minConfidence: number;
    peopleInFrame: number;
}

export interface IActivityHistory {
    compliant: number[];
    violation: number[];
    override: number[];
}

export interface ICamera {
    id: string;
    name: string;
    state: CameraState
    compliantCount: number;
    violationCount: number;
    overrideCount: number;
}
