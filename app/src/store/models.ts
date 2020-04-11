/*
 * SmartCam
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export type ActivityType = "compliant" | "violation" | "override";

export interface IActivity {
    id: string;
    type: ActivityType;
    timestamp: Date;
    camera: string;
    photoUrl: string;
}
