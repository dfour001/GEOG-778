DROP TABLE IF EXISTS formats;
DROP TABLE IF EXISTS servicecontours;
DROP TABLE IF EXISTS stations;

CREATE TABLE Stations (
  callsign varchar,
  frequency varchar,
  service varchar,
  directional varchar,
  fmStatus varchar,
  city varchar,
  state varchar,
  country varchar,
  fileNumber varchar,
  erpHorizontal varchar,
  erpVertical varchar,
  haatHorizonal varchar,
  haatVertical varchar,
  ID varchar,
  dist_40dBu double precision,
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
  applicationID int,
  service varchar,
  lmsApplication varchar,
  dtsSiteNumber varchar,
  transmitterLat double precision,
  transmitterLng double precision,
  wtk varchar,
  geom Geometry
);

CREATE TABLE Formats (
  callsign varchar,
  format varchar
);
