<template>
  <div class="container-fluid">
    <!--Page Content-->
    <card class="card-user where-is-my-thief-container-avatar" v-bind="form">
      <!--Deviceimage which is just stored locally for ecological reasons-->
      <div class="author">
        <b-avatar
          badge-variant="info"
          size="7rem"
          icon="bicycle"
          :src="form.image"
        >
          <template #badge size="50"
            ><b-icon
              v-on:click="invokeImageFileSelection"
              icon="pencil"
            ></b-icon
          ></template>
        </b-avatar>

        <!-- Accept specific image formats by IANA type -->
        <b-form-file
          v-show="false"
          id="imgDeviceFile"
          accept="image/jpeg, image/png"
          @change="onChangeDeviceImage"
        ></b-form-file>
      </div>

      <!--Actucal Form-->
      <b-form @submit="onUpdateDeviceSettings">
        <!--DeviceName-->
        <b-form-group
          id="input-group-update-device-name"
          label="Device Name:"
          label-for="input-update-device-name"
          description='Choose a cool name of your "My Thief"-Device!'
        >
          <b-form-input
            id="input-update-device-name"
            v-model="form.name"
            placeholder="Enter a cool Name..."
            required
          ></b-form-input>
        </b-form-group>

        <!--IMEI-->
        <b-form-group
          id="input-group-update-device-imei"
          label="IMEI:"
          label-for="input-update-device-imei"
          description="On your SIM-Card you will find your IMEI Number. Withour that number the My-Thieve cannot dial in to the Web or receive SMS!"
        >
          <a
            href="https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity"
          >
            What is the SIM-Cards IMEI?
          </a>
          <b-form-input
            id="input-update-device-imei"
            v-model="form.imei"
            placeholder="Enter IMEI..."
            required
          ></b-form-input>
        </b-form-group>

        <!--Device-Tel-->
        <b-form-group
          id="input-group-update-device-tel"
          label="My-Thieves Telephonenumber:"
          label-for="input-update-device-tel"
          description="The number of your My-Thieves SIM-Card. If you want to send SMS's to configure your My-Thieve"
        >
          <b-form-input
            id="input-update-device-tel"
            v-model="form.deviceTel"
            placeholder="Enter Telnnumber: +49..."
            type="tel"
            required
          ></b-form-input>
        </b-form-group>

        <!--SIM-PIN-->
        <b-form-group
          id="input-group-update-device-pin"
          label="My-Thieves SIM-PIN:"
          label-for="input-update-device-pin"
          description="To activate your SIM-Card we need it's PIN in it's Configuration."
        >
          <b-form-input
            id="input-update-device-pin"
            v-model="form.pin"
            placeholder="XXXX"
            type="tel"
            size="4"
            maxlength="4"
            required
          ></b-form-input>
        </b-form-group>

        <!--APN-->
        <b-form-group
          id="input-group-update-device-apn"
          label="My-Thieves APN:"
          label-for="input-group-update-device-apn"
          description="With this information is is possible to dial in to your providers network."
        >
          <a href="https://en.wikipedia.org/wiki/Access_Point_Name">
            What is an APN?
          </a>
          <b-form-input
            id="input-group-update-device-apn"
            v-model="form.apn"
            placeholder="internet"
            required
          >
          </b-form-input>
        </b-form-group>

        <!--APNUSER-->
        <b-form-group
          id="input-group-update-device-apn-user"
          label="My-Thieves APN-User:"
          label-for="input-group-update-device-apn-user"
          description="With this information is is possible to dial in to your providers network."
        >
          <a href="https://en.wikipedia.org/wiki/Access_Point_Name">
            What is an APN?
          </a>
          <b-form-input
            id="input-group-update-device-apn-user"
            v-model="form.apnUser"
            placeholder="internet"
            required
          >
          </b-form-input>
        </b-form-group>

        <!--APNPASSWORD-->
        <b-form-group
          id="input-group-update-device-apn-password"
          label="My-Thieves APN-Password:"
          label-for="input-group-update-device-apn-password"
          description="With this information is is possible to dial in to your providers network."
        >
          <a href="https://en.wikipedia.org/wiki/Access_Point_Name">
            What is an APN?
          </a>
          <b-form-input
            id="input-group-update-device-apn-password"
            v-model="form.apnPassword"
            placeholder="internet"
            required
          >
          </b-form-input>
        </b-form-group>

        <!--Submit Button-->
        <b-button block type="submit" variant="primary">Save changes</b-button>
        <b-button block v-b-modal.deleteDeviceModal variant="danger">
          Delete this Device
        </b-button>
      </b-form>

      <!--Debug Stuff-->
      <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
        <pre class="m-0">{{ form }}</pre>
        <b-button @click="onReset" block variant="danger">Reset</b-button>
      </b-card>
    </card>

    <!--Page Modals-->
    <div class="modals">
      <!--Delete user Modal-->
      <b-modal
        id="deleteDeviceModal"
        title="Do you really want to delete thid Device?"
        hide-footer
        size="sm"
      >
        <!--Download Config file-->
        <b-button class="mt-3" variant="danger" block @click="deleteDevice">
          Delete this device permanently
        </b-button>

        <!--Close Modal-->
        <b-button
          class="mt-3"
          block
          @click="$bvModal.hide('deleteDeviceModal')"
        >
          Cancel
        </b-button>
      </b-modal>
    </div>

    <div class="toasts">
      <!--Toast delete Deivce error-->
      <b-toast
        id="delete-device-error-toast"
        variant="warning"
        solid
        toaster="b-toaster-bottom-center"
        title="Login error"
      >
        <template #toast-title>
          <div class="d-flex flex-grow-1 align-items-baseline">
            <strong class="mr-auto">Deletion failed</strong>
          </div>
        </template>
        Ther was an error when trying to delete Devicedata from your account
      </b-toast>

      <!--Toast delete Device success-->
      <b-toast
        id="delete-device-toast"
        variant="success"
        solid
        toaster="b-toaster-bottom-center"
        title="Login error"
      >
        <template #toast-title>
          <div class="d-flex flex-grow-1 align-items-baseline">
            <strong class="mr-auto">Deletion complete</strong>
          </div>
        </template>
        The Device has been deleted successfully from your account
      </b-toast>

      <!--Toast update device error-->
      <b-toast
        id="update-device-error-toast"
        variant="warning"
        solid
        toaster="b-toaster-bottom-center"
        title="Login error"
      >
        <template #toast-title>
          <div class="d-flex flex-grow-1 align-items-baseline">
            <strong class="mr-auto">Updated Device data failed</strong>
          </div>
        </template>
        An error occured when updating Devicedata. IMEI shall be unique. Device
        name as well.
      </b-toast>

      <!--Toast update device success-->
      <b-toast
        id="update-device-toast"
        variant="success"
        solid
        toaster="b-toaster-bottom-center"
        title="Login error"
      >
        <template #toast-title>
          <div class="d-flex flex-grow-1 align-items-baseline">
            <strong class="mr-auto">Updated Device data successfully</strong>
          </div>
        </template>
        Your Device data is now saved within the Database. To complete
        Configuration update your device in deviceoverview!
      </b-toast>

      <!--Toast update device success-->
      <b-toast
        id="update-device-image-toast"
        variant="success"
        solid
        toaster="b-toaster-bottom-center"
        title="Login error"
      >
        <template #toast-title>
          <div class="d-flex flex-grow-1 align-items-baseline">
            <strong class="mr-auto">Updated Device image successfully</strong>
          </div>
        </template>
        You successfully updated the device image
      </b-toast>
    </div>
  </div>
</template>

<script>
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  name: "update-device-page",
  components: {},
  data() {
    return {
      form: {
        name: "",
        imei: "",
        deviceTel: "",
        image: "",
        apn: "",
        apnUser: "",
        apnPassword: "",
        pin: ""
      }
    };
  },
  methods: {
    /**
     * Debug only, resets the json Object which wold be sended to server
     */
    onReset() {
      // Reset our form values
      this.form = {
        name: "",
        imei: "",
        deviceTel: "",
        image: "",
        apn: "",
        apnUser: "",
        apnPassword: "",
        pin: ""
      };

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },

    /**
     * Methods invokes the hidden
     * fileselsction element so we
     * can use a generic HTML-Element
     * for fileselection
     */
    invokeImageFileSelection() {
      document.getElementById("imgDeviceFile").click();
    },

    /**
     * Callback Method when fileselection
     * for the Porfileimage ws completed.
     * Saves the choosen image to localstorage
     */
    onChangeDeviceImage(event) {
      var self = this;
      const image = event.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = event => {
        this.previewImage = event.target.result;
        this.$bvToast.show("update-device-image-toast");
        localStorage.setItem(
          `devices/${self.form.imei}/image`,
          event.target.result
        );
        self.form.image = localStorage.getItem(
          `devices/${self.form.imei}/image`
        );
      };
    },

    /**
     * Attempts a update of the Server Device object
     */
    onUpdateDeviceSettings(event) {
      //event.preventDefault();
      let apiInstance = new Client.DevicesApi();

      this.$bvModal.show("loading-modal");

      //Create Device Object
      var device = new Client.Device();
      device = {
        imei: this.form.imei,
        pin: this.form.pin,
        apn: this.form.apn,
        apnUser: this.form.apnUser,
        apnPassword: this.form.apnPassword,
        devicePhoneNumber: this.form.deviceTel,
        owner: localStorage.getItem("id"),
        name: this.form.name,
        locations: [],
        ownerPhoneNumber: localStorage.getItem("phonenumber"),
        battery: localStorage.getItem("battery")
      };
      apiInstance
        .updateDevice(this.$route.params.id, { device: device })
        .then(data => {
          console.log("update completed");
          console.log("data,imei ", this.$route.params.id);
          this.getCurrentDeviceData();

          this.$router.push(`/devices/${data.imei}`);
          this.$bvModal.hide("loading-modal");
        });

      this.$bvModal.hide("loading-modal");
    },

    /**
     *
     */
    deleteDevice(event) {
      console.log("Try deleting this device...");
      this.$bvModal.show("loading-modal");

      event.preventDefault();
      var self = this;
      let apiInstance = new Client.DevicesApi();
      apiInstance
        .devicesImeiDelete(this.$route.params.id)
        .then(data => {
          this.$bvModal.hide("loading-modal");
          console.log("Try deleting this device...Succussful");
          this.$bvToast.show("delete-device-toast");
          setTimeout(
            this.$router.push(`/users/${localStorage.getItem("username")}`),
            2000
          );
        })
        .catch(err => {
          this.$bvModal.hide("loading-modal");
          console.log("Try deleting this device...Failed");
          this.$bvToast.show("delete-device-error-toast");
        });
    },

    /**
     * Collects all data of a device and sets
     * the local form model of this component
     */
    getCurrentDeviceData() {
      console.log("Getting current deivcedata...");
      var self = this;
      let apiInstance = new Client.DevicesApi();
      apiInstance
        .devicesImeiGet(this.$route.params.id)
        .then(data => {
          self.form = {
            image: localStorage.getItem(`devices/${data.imei}/image`),

            name: data.name,
            imei: data.imei,
            deviceTel: data.devicePhoneNumber,
            pin: data.pin,
            apn: data.apn,
            apnPassword: data.apnPassword,
            apnUser: data.apnUser
          };

          console.log("Getting current deivcedata...Successful");
        })
        .catch(err => {
          console.log("Getting current deivcedata...Failed");
        });
    }
  },
  mounted: function() {
    this.getCurrentDeviceData();
  }
};
</script>

<style></style>
