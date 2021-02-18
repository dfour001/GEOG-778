DROP TABLE IF EXISTS formats;
DROP TABLE IF EXISTS servicecontours;
DROP TABLE IF EXISTS stations;

CREATE TABLE Stations (
  callsign varchar PRIMARY KEY,
  frequency varchar,
  service varchar,
  directional varchar,
  operation varchar,
  stationClass varchar,
  intStationClass varchar,
  fmStatus varchar,
  city varchar,
  state varchar,
  country varchar,
  fileNumber varchar,
  erpHorizontal varchar,
  erpVertical varchar,
  haatHorizonal varchar,
  haatVertical varchar,
  ID int,
  lat varchar,
  latD double precision,
  latM double precision,
  latS double precision,
  lng varchar,
  lngD double precision,
  lngM double precision,
  lngS double precision,
  licensee varchar
);

CREATE TABLE ServiceContours (
  applicationID int PRIMARY KEY,
  service varchar,
  lmsApplication varchar,
  dtsSiteNumber varchar,
  transmitterLat double precision,
  transmitterLng double precision,
  geom Geometry
);

CREATE TABLE Formats (
  callsign varchar PRIMARY KEY,
  format varchar
);
