import pymongo
from unittest import TestCase
import unittest
import os
import json
import datetime
import time

from pymongo import response

from main import app

class TestCase(TestCase):

    # setup some variables like the usercredentials, device-variables and test-locations
    def setUp(self):
        self.tester = app.test_client(self)
        # self.user_cred = json.dumps(
        #     dict(name="niklas", password="1234Bier"))

        self.user_cred = {"name": "niklas", "password": "1234Bier"}
        self.user_cred_2 = {"name": "niklasus", "password": "1234Bier"}

     # teardown after all test, clear database entries

    def tearDown(self) -> None:

        ##############################################
        # Init DB
        try:

            if os.environ.get("DATABASE_IP") is not None:
                db_location = os.environ["DATABASE_IP"] + ":27017"
            else:
                db_location = "localhost:27017"

            mongo = pymongo.MongoClient(
                db_location, serverSelectionTimeoutMS=1000)
            db = mongo.smts

        except pymongo.errors.ConnectionFailure as err:

            if os.environ.get("DATABASE_IP") is not None:
                db_location = os.environ["DATABASE_IP"] + ":27017"
            else:
                db_location = "localhost:2017"

            print(
                "Trying to connect to Device-DB located at: "
                + db_location
                + "...Failed...Err: "
                + err
            )
            exit(1)

        coll = db["devices"]
        coll.delete_many({"owner": "4242b02caff54df781f8a93c5661c91c"})


############################## helper functions ##########################

    def login_user(self, user_cred=None):

        if user_cred == None:

            user_cred = self.user_cred

        response = self.tester.post(
            '/v1/users/login', data=json.dumps(user_cred), content_type='application/json')

        return response

    def logout_user(self):
        return self.tester.post('/v1/users/logout')

    def remove_user(self, user_id):
        return self.tester.delete(f'/v1/users/{user_id}')

    def add_device(self):
        tmp_device = {
            "name": "device1",
            "imei": "12345",
            "owner": "string",
            "devicePhoneNumber": "017812345",
            "pin": "1111",
            "apn": "apnNumber",
            "apnUser": "apnUsernumber",
            "apnPassword": "apnpassword",
            "ownerPhoneNumber": "string",
            "battery": 0,
            "locations": [
                {
                    "latitude": 0,
                    "longitude": 0,
                    "height": 0,
                    "time": "2021-09-05T11:25:14.241Z",
                    "velocity": 0
                }
            ]
        }

        # send complete device data
        return self.tester.post(
            '/v1/devices', data=json.dumps(tmp_device), content_type="application/json")

    def delete_device(self, imei):
        return self.tester.delete(f'/v1/devices/{imei}')

    def add_device_location(self, imei):

        test_loc = {
            "latitude": 51.241478,
            "longitude": 6.7197800,
            "velocity": 0.00,
            "battery": 55,
            "time": "2021-9-1 10:11:58.00"
        }

        return self.tester.post(
            f'/v1/devices/{imei}/locations', data=json.dumps(test_loc), content_type="application/json")

    def add_device_locations(self, imei):
        'Create about 120 entries beginning from 2 hours ago'
        end = datetime.datetime.now()
        delta_start = datetime.timedelta(hours=2)
        start = end - delta_start
        delta_add = datetime.timedelta(minutes=1)
        this_time = start+delta_add
        for i in range(120):

            test_loc = {
                "latitude": 51.241478,
                "longitude": 6.7197800,
                "velocity": 0.00,
                "battery": 55,
                "time": f"{end.year}-{end.month}-{end.day} {this_time.time()}"
            }
            this_time = this_time+delta_add
            self.tester.post(
                f'/v1/devices/{imei}/locations', data=json.dumps(test_loc), content_type="application/json")

########################### tests #####################################
# USERS
# xxxxx POST ​/users create new User
# xxxxx POST ​/users​/login login an existing User (!)
# xxxxx POST ​/users​/logout logout user
# xxxxx GET ​/users​/{userId} get User by ID
# xxxxx PUT ​/users​/{userId} Update User
# xxxxx DELETE ​/users​/{userId} delete User
# xxxxx GET ​/users​/{userId}​/devices get Devices from User
# DEVICES
# xxxxx POST ​/devices add a new device
# xxxxx GET ​/devices​/{imei} get Device by ID
# xxxxx PUT ​/devices​/{imei} Update Device
# xxxxx DELETE ​/devices​/{imei} delete a device
# GET ​/devices​/{imei}​/status get status of device (!)
# xxxxx POST ​/devices​/{imei}​/locations add GPS-Position to Device
# GET ​/devices​/{imei}​/locations Get Locations of device
# DELETE ​/devices​/{imei}​/locations delete GPSPositions of device

    def test_index(self):

        response = self.tester.get('/v1/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'alive', response.data)

    # check user POST /users
    # should return 201 and new userid
    # should return any 409 and message if name already taken, information not complete
    def test_user_create(self):

        # create new user in database correct
        user_data = {
            "name": "test_user_create",
            "password": "1234Bier",
            "phoneNumber": "0178/7861070"
        }
        response = self.tester.post(
            '/v1/users', data=json.dumps(user_data), content_type='application/json')

        user_id = response.json["_id"]
        self.assertEqual(response.status_code, 201)
        self.assertIn(user_data["name"], response.json["name"])
        self.assertNotIn('password', response.json)

        # check if post with same credentials leads to 409, username already taken
        response_user_taken = self.tester.post(
            '/v1/users', data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response_user_taken.status_code, 409)
        self.assertIn(b'Username already taken!', response_user_taken.data)

        # check if post with insufficient data leads to 409, There is some information missing!
        user_data_incomplete = {
            "name": "test_user_create",
            "phoneNumber": "0178/7861070"
        }

        response_user_incomplete = self.tester.post(
            '/v1/users', data=json.dumps(user_data_incomplete), content_type='application/json')

        self.assertEqual(response_user_incomplete.status_code, 409)
        self.assertIn(b'There is some information missing!',
                      response_user_incomplete.data)

        # delete test_user_create after all tests are finished
        self.remove_user(user_id)

    # check if login behaves correctly with right credentials: response code: 200; correct name in response.json

    def test_login_correct(self):

        username = self.user_cred["name"]

        response = self.tester.post(
            '/v1/users/login', data=json.dumps(self.user_cred), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(username, response.json['name'])

    # check if login behaves correctly when credentials are wrong: status code: 401; "Login Failed" in response.data
    # check if login is rejected when id is wrong

    def test_login_incorrect(self):

        wrong_user = {"name": "not_a_name", "password": "wrongPw"}

        response = self.tester.post(
            '/v1/users/login', data=json.dumps(wrong_user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Login Failed", response.data)

    # check if logout is correct if a person is logged in, and if status 401 if not logged in

    def test_logout(self):

        # login a user
        login_response = self.login_user()

        # log out user, should be successfull
        response_true = self.tester.post(
            '/v1/users/logout')
        self.assertEqual(response_true.status_code, 200)
        self.assertIn(b'Logged out successfully', response_true.data)

        # no user is logged in, logout should be 401
        response_false = self.tester.post(
            '/v1/users/logout')
        self.assertEqual(response_false.status_code, 401)
        self.assertIn(b'Login first', response_false.data)

    # test GET /users/<id>
    # if logged in and correct id: 200 and correct user data
    # if logged in and wring id: 404, text

    def test_get_user(self):

        # login correct user and try to get his data, status code should be 200 and his id should be in the response json
        user_response = self.login_user()
        user_id = user_response.json["_id"]
        response = self.tester.get(f'/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(user_id, response.json["_id"])

        # check wether a logged in user can get data from another person
        other_user_id = "fdcb83bb3c294052b99505d4d5a0e271"
        response_other_user = self.tester.get(f'/v1/users/{other_user_id}')
        self.assertEqual(response_other_user.status_code, 405)
        self.assertIn(b'Not allowed', response_other_user.data)

        # check wether a logged out user can get data from any id
        self.logout_user()
        response_no_user = self.tester.get(f'/v1/users/{other_user_id}')
        self.assertEqual(response_no_user.status_code, 401)
        self.assertIn(b'Login first', response_no_user.data)

    # test PUT /users/id
    # check wether a logged in user can update himself, 201 userdata without password
    # check wether he needs to be logged in, 405 Login first
    # check wether he can change other user data, 405 Not allowed

    def test_update_user(self):
        old_user = self.login_user().json
        old_user["password"] = self.user_cred["password"]

        # check name change
        new_user = old_user
        new_user["name"] = "newname"
        new_user["phoneNumber"] = "1113333"
        response = self.tester.put(
            f'/v1/users/{old_user["_id"]}', data=json.dumps(new_user), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertIn(new_user["name"], response.json["name"])
        self.assertNotIn("password", response.json)

        # check forbidden change of other user
        new_user["name"] = self.user_cred["name"]

        new_user["_id"] = "fdcb83bb3c294052b99505d4d5a0e271"
        response2 = self.tester.put(
            f'/v1/users/{new_user["_id"]}', data=json.dumps(new_user), content_type="application/json")

        self.assertEqual(response2.status_code, 405)
        self.assertIn(b"Not allowed", response2.data)

        # reset changes to standard user
        old_user["_id"] = response.json["_id"]
        self.tester.put(
            f'/v1/users/{old_user["_id"]}', data=json.dumps(old_user), content_type="application/json")

        # logout and try to change again, should be forbidden
        self.logout_user()
        response3 = self.tester.put(
            f'/v1/users/{old_user["_id"]}', data=json.dumps(old_user), content_type="application/json")
        self.assertEqual(response3.status_code, 401)
        self.assertIn(b"Login first", response3.data)

        # Delete User
        # should be forbidden if not logged in, 401 Login first
        # should be forbidden if sessionId != pathid, 405 Not allowed
        # success if logged in and right id, 200 User deleted

    def test_delete_user(self):
        # create temporary user
        user_data = {
            "name": "test_user_delete",
            "password": "1234Bier",
            "phoneNumber": "0178/7861070"
        }
        response_user = self.tester.post(
            '/v1/users', data=json.dumps(user_data), content_type='application/json')

        user_id = response_user.json["_id"]
        wrong_id = "fdcb83bb3c294052b99505d4d5a0e271"

        # test wrong userid
        response = self.tester.delete(f'v1/users/{wrong_id}')
        self.assertEqual(response.status_code, 405)
        self.assertIn(b'Not allowed', response.data)

        # test success
        response2 = self.tester.delete(f'/v1/users/{user_id}')
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'User deleted', response2.data)

        # test if not logged in
        response3 = self.tester.delete(f'/v1/users/{wrong_id}')
        self.assertEqual(response3.status_code, 401)
        self.assertIn(b'Login first', response3.data)

    # test get device list
    # if logged in and correct number 200, json list
    # if not logged in 401, Not allowed

    def test_devices_user(self):
        # login and add device
        user_response = self.login_user()
        device_response = self.add_device()

        # test if status_code ok and imei is in response
        response = self.tester.get(
            f'/v1/users/{user_response.json["_id"]}/devices')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json[0]["imei"], device_response.json["imei"])

        # logout and try again, should be forbidden
        self.logout_user()

        response2 = self.tester.get(
            f'/v1/users/{user_response.json["_id"]}/devices')
        self.assertEqual(response2.status_code, 401)
        self.assertIn(b'Login first', response2.data)


# devices

    # test add new device
    # wrong data, 409 "There is some imformation missing"
    # successfull, 201 devicedata as json

    def test_add_device(self):
        # login and add tmp device to account
        response_user = self.login_user()

        tmp_device = {
            "name": "device1",
            "imei": "12345",
            "owner": "string",
            "devicePhoneNumber": "017812345",
            "pin": "1111",
            "apn": "apnNumber",
            "apnUser": "apnUsernumber",
            "apnPassword": "apnpassword",
            "ownerPhoneNumber": "string",
            "battery": 0,
            "locations": [
                {
                    "latitude": 0,
                    "longitude": 0,
                    "height": 0,
                    "time": "2021-09-05T11:25:14.241Z",
                    "velocity": 0
                }
            ]
        }

        # send complete device data
        response = self.tester.post(
            '/v1/devices', data=json.dumps(tmp_device), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertIn(response_user.json["_id"], response.json["owner"])
        self.assertListEqual([], response.json["locations"])

        # check if rejected if name, imei or phonenumber exists
        response2 = self.tester.post(
            '/v1/devices', data=json.dumps(tmp_device), content_type="application/json")

        self.assertEqual(response2.status_code, 409)
        self.assertIn(b'already exists', response2.data)
        # delete device at the end

    # check if added device can be retrieved
    # if ok, 200 and json data
    # not logged in, 401 Login first
    # not owner of device, 405 Not allowed

    def test_get_device(self):
        user_response = self.login_user()
        device_response = self.add_device()

        # test with everything ok
        response = self.tester.get(
            f'/v1/devices/{device_response.json["imei"]}')
        self.assertEqual(200, response.status_code)
        self.assertIn("ownerPhoneNumber", response.json)

        # test with user not logged in
        self.logout_user()
        response1 = self.tester.get(
            f'/v1/devices/{device_response.json["imei"]}')
        self.assertEqual(401, response1.status_code)
        self.assertIn(b"Login first", response1.data)

        # test with wrong user
        self.login_user(self.user_cred_2)

        response2 = self.tester.get(
            f'/v1/devices/{device_response.json["imei"]}')
        self.assertEqual(405, response2.status_code)
        self.assertIn(b'Not allowed', response2.data)

    # test device update
    # if everything ok, 200 json data
    # if not logged in, 401 Login first
    # if user is not owner, 405 not allowed

    def test_update_device(self):
        self.login_user()
        device_response = self.add_device()
        device_update = device_response.json
        device_update["name"] = "test_update_name"

        # test everythin ok
        response = self.tester.put(f'/v1/devices/{device_update["imei"]}', data=json.dumps(
            device_update), content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertIn(device_update["name"], response.json["name"])

        # test not logged in
        self.logout_user()
        response2 = self.tester.put(f'/v1/devices/{device_update["imei"]}', data=json.dumps(
            device_update), content_type="application/json")
        self.assertEqual(401, response2.status_code)
        self.assertIn(b'Login first', response2.data)

        # test wrong user/device

        self.login_user(self.user_cred_2)
        response3 = self.tester.put(f'/v1/devices/{device_update["imei"]}', data=json.dumps(
            device_update), content_type="application/json")
        self.assertEqual(405, response3.status_code)
        self.assertIn(b'Not allowed', response3.data)

    # test ok, 200 device deleted succesfully
    # not logged in, 401 Login first
    # not owner of device, 405 Not allowed

    def test_delete_device(self):
        self.login_user()
        device_response = self.add_device()

        # test everythin ok
        response = self.tester.delete(
            f'/v1/devices/{device_response.json["imei"]}')
        self.assertEqual(200, response.status_code)
        self.assertIn(b'successfully', response.data)

        # add new device, log out and try again
        device_response = self.add_device()
        self.logout_user()
        response2 = self.tester.delete(
            f'/v1/devices/{device_response.json["imei"]}')
        self.assertEqual(401, response2.status_code)
        self.assertIn(b'Login first', response2.data)

        # login other user, should return 405 Not Allowed
        self.login_user(self.user_cred_2)
        response3 = self.tester.delete(
            f'/v1/devices/{device_response.json["imei"]}')
        self.assertEqual(405, response3.status_code)
        self.assertIn(b'Not allowed', response3.data)
        self.logout_user()

        # ok, 201 json data
        # not all needed data, 409 Information missing
        # imei not correct, 409 Couldn't retrieve device data from DB
        # db error, 409 Location couldn't be added to DB

    def test_device_add_location(self):
        self.login_user()
        device_response = self.add_device()

        test_loc = {
            "latitude": 51.241478,
            "longitude": 6.7197800,
            "velocity": 0.00,
            "battery": 55,
            "time": "2021-9-1 10:11:58.00"
        }

        response = self.tester.post(
            f'/v1/devices/{device_response.json["imei"]}/locations', data=json.dumps(test_loc), content_type="application/json")
        self.assertEqual(201, response.status_code)
        self.assertIn(test_loc["time"], response.json["time"])

        # test for missing information
        test_loc2 = test_loc.copy()
        del test_loc2["latitude"]

        response2 = self.tester.post(
            f'/v1/devices/{device_response.json["imei"]}/locations', data=json.dumps(test_loc2), content_type="application/json")
        self.assertEqual(409, response2.status_code)
        self.assertIn(b'informations missing', response2.data)

        # test for incorrect imei

        response3 = self.tester.post(
            f'/v1/devices/12345678/locations', data=json.dumps(test_loc), content_type="application/json")
        self.assertEqual(409, response3.status_code)
        self.assertIn(b'retrieve device data from DB', response3.data)

    # ok, 200 json data
    # not logged in, 401 Login first
    # not correct user, 405 Not allowed
    # no locations, 404 No locations

    def test_device_get_locations(self):
        self.login_user()
        device_response = self.add_device()

        # check empty locations
        response = self.tester.get(
            f'/v1/devices/{device_response.json["imei"]}/locations')
        self.assertEqual(204, response.status_code)
        self.assertIn(b'', response.data)

        # add loc and test ok
        self.add_device_location(device_response.json["imei"])
        self.add_device_location(device_response.json["imei"])
        response2 = self.tester.get(
            f'/v1/devices/{device_response.json["imei"]}/locations')
        self.assertEqual(200, response2.status_code)
        self.assertIn("latitude", response2.json[0])
        self.assertIn("longitude", response2.json[0])

        # logout and check 401, Login first
        self.logout_user()

        response3 = self.tester.get(
            f'/v1/devices/{device_response.json["imei"]}/locations')
        self.assertEqual(401, response3.status_code)
        self.assertIn(b'Login first', response3.data)

        # login wrong user, 405 Not allowed
        self.login_user(self.user_cred_2)
        response4 = self.tester.get(
            f'/v1/devices/{device_response.json["imei"]}/locations')
        self.assertEqual(405, response4.status_code)
        self.assertIn(b'Not allowed', response4.data)

    def test_device_get_locations_time(self):
        self.login_user()
        dev_resp = self.add_device()
        self.add_device_locations(dev_resp.json["imei"])

        # compute millis with defined timedelta should return the entries from now until x minutes before
        minutes = 60
        minutes_in_millis = minutes*60*1000
        
        end = int(time.time()*1000)
        start = end-minutes_in_millis


        # ok, 200 status in json
        response = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/locations?start={start}&end={end}')
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(minutes, len(response.json))

        # test start but not end
        response = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/locations?start={start}')
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(minutes, len(response.json))
        
         # test end but not start
        
        response = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/locations?end={start}')
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(minutes, len(response.json))

         # test timestamp out of range, 204
        response = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/locations?end={end-start}')
        
        self.assertEqual(204, response.status_code)
        
        


    def test_device_status(self):
        self.login_user()
        dev_resp = self.add_device()

        # test status inactive, 200 "inactive"
        response = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/status')
        self.assertEqual(200, response.status_code)
        
        self.assertIn(b"inactive", response.data)

        self.add_device_location(dev_resp.json["imei"])

        response1 = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/status')
        self.assertEqual(200, response1.status_code)
        self.assertIn(b"active", response1.data)

    # delete positions, 200 "all positions deleted"

    # not logged in, 401 Login first
    # wrong user/device, 405 Not alowed

    def test_device_locations_delete(self):
        self.login_user()
        dev_resp = self.add_device()
        self.add_device_locations(dev_resp.json["imei"])

        # add 120 location entries and make sure they are correct
        response = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/locations')


  
        # logout user, should give 401 Login first
        self.logout_user()
        response = self.tester.delete(
            f'/v1/devices/{dev_resp.json["imei"]}/locations')
        self.assertEqual(401, response.status_code)

        # login other user, should give 405
        self.login_user(self.user_cred_2)
        response = self.tester.delete(
            f'/v1/devices/{dev_resp.json["imei"]}/locations')
        self.assertEqual(405, response.status_code)

        self.logout_user()

        # delete all of them, should be a 200 and afterwards size == 0
        self.login_user()
        response2 = self.tester.delete(
            f'/v1/devices/{dev_resp.json["imei"]}/locations')
        self.assertEqual(200, response2.status_code)

        self.assertEqual(
            b"All device locations deleted successfully", response2.data)

        response3 = self.tester.get(
            f'/v1/devices/{dev_resp.json["imei"]}/locations')
        self.assertIn(b'', response3.data)


if __name__ == "__main__":
    unittest.main()
