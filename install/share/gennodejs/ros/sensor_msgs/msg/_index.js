
"use strict";

let MagneticField = require('./MagneticField.js');
let NavSatFix = require('./NavSatFix.js');
let RelativeHumidity = require('./RelativeHumidity.js');
let Range = require('./Range.js');
let MultiDOFJointState = require('./MultiDOFJointState.js');
let JoyFeedback = require('./JoyFeedback.js');
let CameraInfo = require('./CameraInfo.js');
let Imu = require('./Imu.js');
let LaserEcho = require('./LaserEcho.js');
let NavSatStatus = require('./NavSatStatus.js');
let PointCloud2 = require('./PointCloud2.js');
let ChannelFloat32 = require('./ChannelFloat32.js');
let BatteryState = require('./BatteryState.js');
let Temperature = require('./Temperature.js');
let Illuminance = require('./Illuminance.js');
let Joy = require('./Joy.js');
let RegionOfInterest = require('./RegionOfInterest.js');
let MultiEchoLaserScan = require('./MultiEchoLaserScan.js');
let FluidPressure = require('./FluidPressure.js');
let LaserScan = require('./LaserScan.js');
let JointState = require('./JointState.js');
let PointCloud = require('./PointCloud.js');
let Image = require('./Image.js');
let JoyFeedbackArray = require('./JoyFeedbackArray.js');
let CompressedImage = require('./CompressedImage.js');
let TimeReference = require('./TimeReference.js');
let PointField = require('./PointField.js');

module.exports = {
  MagneticField: MagneticField,
  NavSatFix: NavSatFix,
  RelativeHumidity: RelativeHumidity,
  Range: Range,
  MultiDOFJointState: MultiDOFJointState,
  JoyFeedback: JoyFeedback,
  CameraInfo: CameraInfo,
  Imu: Imu,
  LaserEcho: LaserEcho,
  NavSatStatus: NavSatStatus,
  PointCloud2: PointCloud2,
  ChannelFloat32: ChannelFloat32,
  BatteryState: BatteryState,
  Temperature: Temperature,
  Illuminance: Illuminance,
  Joy: Joy,
  RegionOfInterest: RegionOfInterest,
  MultiEchoLaserScan: MultiEchoLaserScan,
  FluidPressure: FluidPressure,
  LaserScan: LaserScan,
  JointState: JointState,
  PointCloud: PointCloud,
  Image: Image,
  JoyFeedbackArray: JoyFeedbackArray,
  CompressedImage: CompressedImage,
  TimeReference: TimeReference,
  PointField: PointField,
};
