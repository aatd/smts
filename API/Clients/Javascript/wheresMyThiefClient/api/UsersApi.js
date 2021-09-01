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
import {User} from '../model/User';

/**
* Users service.
* @module api/UsersApi
* @version 1.0
*/
export class UsersApi {

    /**
    * Constructs a new UsersApi. 
    * @alias module:api/UsersApi
    * @class
    * @param {module:ApiClient} [apiClient] Optional API client implementation to use,
    * default to {@link module:ApiClient#instance} if unspecified.
    */
    constructor(apiClient) {
        this.apiClient = apiClient || ApiClient.instance;
    }



    /**
     * create new User
     * Function to create a new user in the database. Requires Parameters: 'name', 'password', 'phonenumber'. If the registration is succesful, a 'User' element is returned
     * @param {module:model/User} user 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing data of type {@link module:model/User} and HTTP response
     */
    createUserWithHttpInfo(user) {
      let postBody = user;

      // verify the required parameter 'user' is set
      if (user === undefined || user === null) {
        throw new Error("Missing the required parameter 'user' when calling createUser");
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
      let returnType = User;

      return this.apiClient.callApi(
        '/users', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * create new User
     * Function to create a new user in the database. Requires Parameters: 'name', 'password', 'phonenumber'. If the registration is succesful, a 'User' element is returned
     * @param {module:model/User} user 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with data of type {@link module:model/User}
     */
    createUser(user) {
      return this.createUserWithHttpInfo(user)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * get Devices from User
     * Function to get all 'Devices' from an specific user. Returns an array of 'Devices' from the database.
     * @param {String} userId 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing data of type {@link Array.<module:model/Device>} and HTTP response
     */
    findAllDevicesWithHttpInfo(userId) {
      let postBody = null;

      // verify the required parameter 'userId' is set
      if (userId === undefined || userId === null) {
        throw new Error("Missing the required parameter 'userId' when calling findAllDevices");
      }


      let pathParams = {
        'userId': userId
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
      let returnType = [Device];

      return this.apiClient.callApi(
        '/users/{userId}/devices', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * get Devices from User
     * Function to get all 'Devices' from an specific user. Returns an array of 'Devices' from the database.
     * @param {String} userId 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with data of type {@link Array.<module:model/Device>}
     */
    findAllDevices(userId) {
      return this.findAllDevicesWithHttpInfo(userId)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * get User by ID
     * get a specific user by its unique ID. Returns the user as an 'User' element.
     * @param {String} userId 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing data of type {@link module:model/User} and HTTP response
     */
    getUserbyIdWithHttpInfo(userId) {
      let postBody = null;

      // verify the required parameter 'userId' is set
      if (userId === undefined || userId === null) {
        throw new Error("Missing the required parameter 'userId' when calling getUserbyId");
      }


      let pathParams = {
        'userId': userId
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
      let returnType = User;

      return this.apiClient.callApi(
        '/users/{userId}', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * get User by ID
     * get a specific user by its unique ID. Returns the user as an 'User' element.
     * @param {String} userId 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with data of type {@link module:model/User}
     */
    getUserbyId(userId) {
      return this.getUserbyIdWithHttpInfo(userId)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * login an existing User (!)
     * Function to login an existing User. Checks if the User exists in the database and if the entered password is correct. Returns 'User' element (in : object User??)
     * @param {Object} opts Optional parameters
     * @param {module:model/User} opts.user 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing data of type {@link module:model/User} and HTTP response
     */
    loginUserWithHttpInfo(opts) {
      opts = opts || {};
      let postBody = opts['user'];


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
      let accepts = [];
      let returnType = User;

      return this.apiClient.callApi(
        '/users/login', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * login an existing User (!)
     * Function to login an existing User. Checks if the User exists in the database and if the entered password is correct. Returns 'User' element (in : object User??)
     * @param {Object} opts Optional parameters
     * @param {module:model/User} opts.user 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with data of type {@link module:model/User}
     */
    loginUser(opts) {
      return this.loginUserWithHttpInfo(opts)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * Update User
     * Function to update user information. Updated information will be overwritten in the database. Returns the changed 'User'
     * @param {String} userId 
     * @param {Object} opts Optional parameters
     * @param {module:model/User} opts.user 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing data of type {@link module:model/User} and HTTP response
     */
    updateUserWithHttpInfo(userId, opts) {
      opts = opts || {};
      let postBody = opts['user'];

      // verify the required parameter 'userId' is set
      if (userId === undefined || userId === null) {
        throw new Error("Missing the required parameter 'userId' when calling updateUser");
      }


      let pathParams = {
        'userId': userId
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
      let returnType = User;

      return this.apiClient.callApi(
        '/users/{userId}', 'PUT',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * Update User
     * Function to update user information. Updated information will be overwritten in the database. Returns the changed 'User'
     * @param {String} userId 
     * @param {Object} opts Optional parameters
     * @param {module:model/User} opts.user 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with data of type {@link module:model/User}
     */
    updateUser(userId, opts) {
      return this.updateUserWithHttpInfo(userId, opts)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * logout user
     * Function to logout User from application. 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing HTTP response
     */
    usersLogoutPostWithHttpInfo() {
      let postBody = null;


      let pathParams = {
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
        '/users/logout', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * logout user
     * Function to logout User from application. 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}
     */
    usersLogoutPost() {
      return this.usersLogoutPostWithHttpInfo()
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


    /**
     * delete User
     * Delete an existing User. User must be logged in, to delete its information from the database.
     * @param {String} userId 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}, with an object containing HTTP response
     */
    usersUserIdDeleteWithHttpInfo(userId) {
      let postBody = null;

      // verify the required parameter 'userId' is set
      if (userId === undefined || userId === null) {
        throw new Error("Missing the required parameter 'userId' when calling usersUserIdDelete");
      }


      let pathParams = {
        'userId': userId
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
        '/users/{userId}', 'DELETE',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType
      );
    }

    /**
     * delete User
     * Delete an existing User. User must be logged in, to delete its information from the database.
     * @param {String} userId 
     * @return {Promise} a {@link https://www.promisejs.org/|Promise}
     */
    usersUserIdDelete(userId) {
      return this.usersUserIdDeleteWithHttpInfo(userId)
        .then(function(response_and_data) {
          return response_and_data.data;
        });
    }


}