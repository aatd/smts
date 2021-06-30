/*
 * mythief
 *  API for the Where is my Thief Project
 *
 * OpenAPI spec version: 0.0.6
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 *
 * Swagger Codegen version: 2.4.19
 *
 * Do not edit the class manually.
 *
 */

import {ApiClient} from '../ApiClient';

/**
 * The User model module.
 * @module model/User
 * @version 0.0.6
 */
export class User {
  /**
   * Constructs a new <code>User</code>.
   * @alias module:model/User
   * @class
   */
  constructor() {
  }

  /**
   * Constructs a <code>User</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/User} obj Optional instance to populate.
   * @return {module:model/User} The populated <code>User</code> instance.
   */
  static constructFromObject(data, obj) {
    if (data) {
      obj = obj || new User();
      if (data.hasOwnProperty('id'))
        obj.id = ApiClient.convertToType(data['id'], 'String');
      if (data.hasOwnProperty('name'))
        obj.name = ApiClient.convertToType(data['name'], 'String');
      if (data.hasOwnProperty('password'))
        obj.password = ApiClient.convertToType(data['password'], 'String');
      if (data.hasOwnProperty('phoneNumber'))
        obj.phoneNumber = ApiClient.convertToType(data['phoneNumber'], 'String');
      if (data.hasOwnProperty('devices'))
        obj.devices = ApiClient.convertToType(data['devices'], ['Number']);
    }
    return obj;
  }
}

/**
 * @member {String} id
 */
User.prototype.id = undefined;

/**
 * @member {String} name
 */
User.prototype.name = undefined;

/**
 * @member {String} password
 */
User.prototype.password = undefined;

/**
 * @member {String} phoneNumber
 */
User.prototype.phoneNumber = undefined;

/**
 * @member {Array.<Number>} devices
 */
User.prototype.devices = undefined;


