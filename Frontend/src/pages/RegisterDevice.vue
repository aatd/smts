<template>
  <div class="content">
    <div class="container-fluid">
      <!--Page Content-->
      <card class="card-user where-is-my-thief-container">
        <!--Background Picture-->
        <img slot="image" src="img/logo.png" alt="..." />

        <!--Form to Submit new Deivce to Server-->
        <b-form @submit="registerDevice">
          <!--DeviceName-->
          <b-form-group
            id="input-group-register-device-name"
            label="Device Name:"
            label-for="input-register-device-name"
            description='Choose a Name of your "My Thief"-Device!'
          >
            <b-form-input
              id="input-register-device-name"
              v-model="form.name"
              placeholder="Enter a cool Name..."
              required
            >
            </b-form-input>
          </b-form-group>

          <!--IMEI-->
          <b-form-group
            id="input-group-register-device-imei"
            label="IMEI:"
            label-for="input-register-device-imei"
            description="On your SIM-Card you will find your IMEI Number. Withour that number the My-Thieve cannot dial in to the Web!"
          >
            <a
              href="https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity"
            >
              What is the SIM-Cards IMEI?
            </a>
            <b-form-input
              id="input-register-device-imei"
              v-model="form.imei"
              placeholder="Enter IMEI..."
              type="tel"
              required
            >
            </b-form-input>
          </b-form-group>

          <!--Device-Tel-->
          <b-form-group
            id="input-group-register-device-tel"
            label="My-Thieves Telephonenumber:"
            label-for="input-register-device-tel"
            description="The number of your My-Thieves SIM-Card. If you want to send SMS's to configure your My-Thieve"
          >
            <b-form-input
              id="input-register-device-tel"
              v-model="form.deviceTel"
              placeholder="Enter Telnnumber: +49..."
              type="tel"
              required
            >
            </b-form-input>
          </b-form-group>

          <!--SIM-PIN-->
          <b-form-group
            id="input-group-register-device-pin"
            label="My-Thieves SIM-PIN:"
            label-for="input-register-device-pin"
            description="To activate your SIM-Card we need it's PIN in it's Configuration."
          >
            <b-form-input
              id="input-register-device-pin"
              v-model="form.pin"
              placeholder="XXXX"
              pattern="^[0-9]{4}$"
              maxlength="4"
              required
            >
            </b-form-input>
          </b-form-group>

          <!--APN-->
          <b-form-group
            id="input-group-register-device-apn"
            label="APN:"
            label-for="input-register-device-apn"
            description="The APN is needed to dial in to your providers network."
          >
            <a href="https://en.wikipedia.org/wiki/Access_Point_Name">
              What is an APN?
            </a>
            <b-form-input
              id="input-register-device-apn"
              v-model="form.apn"
              placeholder="Enter the APN of your provider!"
              required
            >
            </b-form-input>
          </b-form-group>

          <!--APN-User-->
          <b-form-group
            id="input-group-register-device-apn-user"
            label="APN-Username:"
            label-for="input-register-device-apn-user"
            description="The APN username is needed to dial in to your providers network."
          >
            <b-form-input
              id="input-register-device-apn-user"
              v-model="form.apnUser"
              placeholder="Enter the APN usrename of your provider!"
              required
            >
            </b-form-input>
          </b-form-group>

          <!--APN-Password-->
          <b-form-group
            id="input-group-register-device-apn-password"
            label="APN-Password:"
            label-for="input-register-device-apn-password"
            description="The APN password is needed to dial in to your providers network."
          >
            <b-form-input
              id="input-register-device-apn-password"
              v-model="form.apnPassword"
              placeholder="Enter the APN password of your provider!"
              required
            >
            </b-form-input>
          </b-form-group>

          <!--Submit Button-->
          <b-button block type="submit" variant="primary">
            RegisterDevice
          </b-button>
        </b-form>

        <!--Debug Stuff-->
        <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
          <pre class="m-0">{{ form }}</pre>
          <b-button @click="onReset" block variant="danger">Reset</b-button>
        </b-card>
      </card>

      <div id="toasts">
        <!--Toast generic login error-->
        <b-toast
          id="register-device-error-toast"
          variant="warning"
          solid
          toaster="b-toaster-bottom-center"
          title="Login error"
        >
          <template #toast-title>
            <div class="d-flex flex-grow-1 align-items-baseline">
              <strong class="mr-auto">Login failed</strong>
            </div>
          </template>
          Couldn't add new Device to your account. Are the name, IMEI, or the
          devices phonenumber already in use?
        </b-toast>
      </div>
    </div>
  </div>
</template>

<script>
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  name: "register-device-page",
  data() {
    return {
      form: {
        name: "",
        imei: "",
        userTel: "",
        deviceTel: "",
        pin: "",
        apn: "",
        apnUser: "",
        apnPassword: "",
      },
    };
  },
  methods: {
    /**
     * Debug only, resets the json Object which wold be sended to server
     */
    onReset() {
      // Reset our form values
      this.form.name = "";
      this.form.imei = "";
      this.form.pin = "";
      this.form.deviceTel = "";
      this.form.apn = "";
      this.form.apnUser = "";
      this.form.apnPassword = "";

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },

    /**
     * Attemps a new device registration on the Server
     */
    registerDevice(event) {
      event.preventDefault();
      var deviceModel = new Client.Device();
      deviceModel.name = this.form.name;
      deviceModel.imei = this.form.imei;
      deviceModel.devicePhoneNumber = this.form.deviceTel;
      deviceModel.apn = this.form.apn;
      deviceModel.apnUser = this.form.apnUser;
      deviceModel.apnPassword = this.form.apnPassword;
      deviceModel.pin = this.form.pin;

      var apiInstance = new Client.DevicesApi();

      apiInstance
        .addDevice(deviceModel)
        .then(() => {
          console.log("Device added successfully.");
          this.$router.push(`/users/${localStorage.getItem("username")}`);
        })
        .catch(() => {
          this.$bvToast.show("register-device-error-toast");
        });
    },
  },
};
</script>

<style>
</style>
