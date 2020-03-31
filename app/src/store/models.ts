/*
 * SmartCam
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export type PerimeterStatus = "alert" | "suspicious" | "clear";

export interface ICamera {
    id: string;
    name: string;
    coordinates: [number, number];
    latestPhotoUrl?: string;
    latestPhotoDateTime?: Date;
}
