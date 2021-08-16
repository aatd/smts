/*
 * Where's my Thief? - API
 *  API zur Webanwendung
 *
 * OpenAPI spec version: 1.0
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 *
 * Swagger Codegen version: 2.4.21
 *
 * Do not edit the class manually.
 *
 */

import {ApiClient} from '../ApiClient';
import {GPSPosition} from './GPSPosition';

/**
 * The Device model module.
 * @module model/Device
 * @version 1.0
 */
export class Device {
  /**
   * Constructs a new <code>Device</code>.
   * @alias module:model/Device
   * @class
   */
  constructor() {
  }

  /**
   * Constructs a <code>Device</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/Device} obj Optional instance to populate.
   * @return {module:model/Device} The populated <code>Device</code> instance.
   */
  static constructFromObject(data, obj) {
    if (data) {
      obj = obj || new Device();
      if (data.hasOwnProperty('name'))
        obj.name = ApiClient.convertToType(data['name'], 'String');
      if (data.hasOwnProperty('imei'))
        obj.imei = ApiClient.convertToType(data['imei'], 'String');
      if (data.hasOwnProperty('owner'))
        obj.owner = ApiClient.convertToType(data['owner'], 'String');
      if (data.hasOwnProperty('devicePhoneNumber'))
        obj.devicePhoneNumber = ApiClient.convertToType(data['devicePhoneNumber'], 'String');
      if (data.hasOwnProperty('ownerPhoneNumber'))
        obj.ownerPhoneNumber = ApiClient.convertToType(data['ownerPhoneNumber'], 'String');
      if (data.hasOwnProperty('battery'))
        obj.battery = ApiClient.convertToType(data['battery'], 'Number');
      if (data.hasOwnProperty('apn'))
        obj.apn = ApiClient.convertToType(data['apn'], 'String');
      if (data.hasOwnProperty('pin'))
        obj.pin = ApiClient.convertToType(data['pin'], 'String');
      if (data.hasOwnProperty('locations'))
        obj.locations = ApiClient.convertToType(data['locations'], [GPSPosition]);
    }
    return obj;
  }
}

/**
 * @member {String} name
 */
Device.prototype.name = undefined;

/**
 * @member {String} imei
 */
Device.prototype.imei = undefined;

/**
 * @member {String} owner
 */
Device.prototype.owner = undefined;

/**
 * @member {String} devicePhoneNumber
 */
Device.prototype.devicePhoneNumber = undefined;

/**
 * @member {String} ownerPhoneNumber
 */
Device.prototype.ownerPhoneNumber = undefined;

/**
 * @member {Number} battery
 */
Device.prototype.battery = undefined;

/**
 * @member {String} apn
 */
Device.prototype.apn = undefined;

/**
 * @member {String} pin
 */
Device.prototype.pin = undefined;

/**
 * @member {Array.<module:model/GPSPosition>} locations
 */
Device.prototype.locations = undefined;


