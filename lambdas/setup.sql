--
-- Contains SQL statements to set up the database.
--

-- noinspection SqlNoDataSourceInspectionForFile

CREATE TABLE cameras
(
    id            uuid                     NOT NULL PRIMARY KEY,
    device_serial character varying(255)   NOT NULL UNIQUE,
    device_name   character varying(255)   NOT NULL,
    pinged_on     timestamp with time zone NOT NULL
);

CREATE TABLE detections
(
    id              uuid                     NOT NULL PRIMARY KEY,
    device_serial   character varying(255)   NOT NULL,
    created_on      timestamp with time zone NOT NULL,
    recorded_on     timestamp with time zone NOT NULL,
    min_confidence  double precision         NOT NULL,
    people_in_frame integer                  NOT NULL,
    activity        character varying(255)   NOT NULL,
    rating          integer                  NOT NULL DEFAULT 0
);

CREATE INDEX CONCURRENTLY serial_index ON cameras (device_serial ASC);
CREATE INDEX CONCURRENTLY recorded_on_index ON detections (recorded_on DESC);
CREATE INDEX CONCURRENTLY serial_index ON detections (device_serial ASC);
