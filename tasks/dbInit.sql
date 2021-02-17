CREATE TABLE "Stations" (
  "callsign" varchar PRIMARY KEY,
  "frequency" varchar,
  "service" varchar,
  "directional" varchar,
  "operation" varchar,
  "stationClass" varchar,
  "intStationClass" varchar,
  "fmStatus" varchar,
  "city" varchar,
  "state" varchar,
  "country" varchar,
  "fileNumber" varchar,
  "erpHorizontal" varchar,
  "erpVertical" varchar,
  "haatHorizonal" varchar,
  "haatVertical" varchar,
  "ID" int,
  "lat" varchar,
  "latD" double,
  "latM" double,
  "latS" double,
  "lng" varchar,
  "lngD" double,
  "lngM" double,
  "lngS" double,
  "licensee" varchar
);

CREATE TABLE "ServiceContours" (
  "applicationID" int PRIMARY KEY,
  "service" varchar,
  "lmsApplication" varchar,
  "dtsSiteNumber" varchar,
  "transmitterLat" double,
  "transmitterLng" double,
  "geom" Geometry
);

CREATE TABLE "ProgrammingFormats" (
  "callsign" varchar PRIMARY KEY,
  "format" varchar
);
