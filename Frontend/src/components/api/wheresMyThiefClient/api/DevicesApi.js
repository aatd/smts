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

import {ApiClient} from "../ApiClient";
import {Device} from '../model/Device';
import {DeviceData} from '../model/DeviceData';
import {GPSPosition} from '../model/GPSPosition';

/**
* Devices service.
* @module api/DevicesApi
* @version 1.0
*/
export class DevicesApi {

    /**
    * Constructs a new DevicesApi. 
    * @alias module:api/DevicesApi
    * @class
    * @param {module:ApiClient} [apiClient] Optional API client implementation to use,
    * default to {@link module:ApiClient#instance} if unspecified.
    */
    constructor(apiClient) {
        this.apiClient = apiClient || ApiClient.instance;
    }



    /**
     * add Device
     * @param {module:model/Device} device 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing HTTP response
     */
    addDeviceWithHttpInfo(device) {
      let postBody = device;

      // verify the required parameter 'device' is set
      if (device === undefined || device === null) {
        throw new Error("Missing the required parameter 'device' when calling addDevice");
      }


      let pathParams = {
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = ['application/json'];
      let accepts = ['application/json'];
      let returnType = null;

      return this.apiClient.callApi(
        '/devices', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * add Device
     * @param {module:model/Device} device 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}
     */
    addDevice(device) {
      return this.addDeviceWithHttpInfo(device)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing HTTP response
     */
    devicesImeiDeleteWithHttpInfo(imei) {
      let postBody = null;

      // verify the required parameter 'imei' is set
      if (imei === undefined || imei === null) {
        throw new Error("Missing the required parameter 'imei' when calling devicesImeiDelete");
      }


      let pathParams = {
        'imei': imei
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = [];
      let returnType = null;

      return this.apiClient.callApi(
        '/devices/{imei}', 'DELETE',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}
     */
    devicesImeiDelete(imei) {
      return this.devicesImeiDeleteWithHttpInfo(imei)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * get Device by ID
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing data of type {@link module:model/DeviceData} and HTTP response
     */
    devicesImeiGetWithHttpInfo(imei) {
      let postBody = null;

      // verify the required parameter 'imei' is set
      if (imei === undefined || imei === null) {
        throw new Error("Missing the required parameter 'imei' when calling devicesImeiGet");
      }


      let pathParams = {
        'imei': imei
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = DeviceData;

      return this.apiClient.callApi(
        '/devices/{imei}', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * get Device by ID
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with data of type {@link module:model/DeviceData}
     */
    devicesImeiGet(imei) {
      return this.devicesImeiGetWithHttpInfo(imei)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing HTTP response
     */
    devicesImeiLocationsDeleteWithHttpInfo(imei) {
      let postBody = null;

      // verify the required parameter 'imei' is set
      if (imei === undefined || imei === null) {
        throw new Error("Missing the required parameter 'imei' when calling devicesImeiLocationsDelete");
      }


      let pathParams = {
        'imei': imei
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = [];
      let returnType = null;

      return this.apiClient.callApi(
        '/devices/{imei}/locations', 'DELETE',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}
     */
    devicesImeiLocationsDelete(imei) {
      return this.devicesImeiLocationsDeleteWithHttpInfo(imei)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * Get Locations of device
     * @param {String} imei 
     * @param {Object} opts Optional parameters
     * @param {String} opts.start If only start value is given, the locations from this date until now are returned. Formatted as specified in ISO 8601
     * @param {String} opts.end If end parameter is given, the locations in between this time frame will be returned.
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing data of type {@link Array.<module:model/GPSPosition>} and HTTP response
     */
    devicesImeiLocationsGetWithHttpInfo(imei, opts) {
      opts = opts || {};
      let postBody = null;

      // verify the required parameter 'imei' is set
      if (imei === undefined || imei === null) {
        throw new Error("Missing the required parameter 'imei' when calling devicesImeiLocationsGet");
      }


      let pathParams = {
        'imei': imei
      };
      let queryParams = {
        'start': opts['start'],
        'end': opts['end']
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = [];
      let returnType = [GPSPosition];

      return this.apiClient.callApi(
        '/devices/{imei}/locations', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * Get Locations of device
     * @param {String} imei 
     * @param {Object} opts Optional parameters
     * @param {String} opts.start If only start value is given, the locations from this date until now are returned. Formatted as specified in ISO 8601
     * @param {String} opts.end If end parameter is given, the locations in between this time frame will be returned.
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with data of type {@link Array.<module:model/GPSPosition>}
     */
    devicesImeiLocationsGet(imei, opts) {
      return this.devicesImeiLocationsGetWithHttpInfo(imei, opts)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * add GPS-Position to Device
     * @param {String} imei 
     * @param {Array.<module:model/GPSPosition>} gpsPosition 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing HTTP response
     */
    devicesImeiLocationsPostWithHttpInfo(imei, gpsPosition) {
      let postBody = gpsPosition;

      // verify the required parameter 'imei' is set
      if (imei === undefined || imei === null) {
        throw new Error("Missing the required parameter 'imei' when calling devicesImeiLocationsPost");
      }

      // verify the required parameter 'gpsPosition' is set
      if (gpsPosition === undefined || gpsPosition === null) {
        throw new Error("Missing the required parameter 'gpsPosition' when calling devicesImeiLocationsPost");
      }


      let pathParams = {
        'imei': imei
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = ['application/json', 'application/x-www-form-urlencoded'];
      let accepts = ['application/json'];
      let returnType = null;

      return this.apiClient.callApi(
        '/devices/{imei}/locations', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * add GPS-Position to Device
     * @param {String} imei 
     * @param {Array.<module:model/GPSPosition>} gpsPosition 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}
     */
    devicesImeiLocationsPost(imei, gpsPosition) {
      return this.devicesImeiLocationsPostWithHttpInfo(imei, gpsPosition)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * get status of device
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing HTTP response
     */
    devicesImeiStatusGetWithHttpInfo(imei) {
      let postBody = null;

      // verify the required parameter 'imei' is set
      if (imei === undefined || imei === null) {
        throw new Error("Missing the required parameter 'imei' when calling devicesImeiStatusGet");
      }


      let pathParams = {
        'imei': imei
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = null;

      return this.apiClient.callApi(
        '/devices/{imei}/status', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * get status of device
     * @param {String} imei 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}
     */
    devicesImeiStatusGet(imei) {
      return this.devicesImeiStatusGetWithHttpInfo(imei)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


}