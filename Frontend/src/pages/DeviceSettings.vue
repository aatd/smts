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
      <b-form @submit="onUpdateDeviceSetings">
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
          label="My-Thieves SIM-PIN:"
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
        pin: "",
        image: "",
        apn: ""
      }
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
    onUpdateDeviceSetings(event) {
      event.preventDefault();
      // No Function is API / Server
    },

    /**
     *
     */
    deleteDevice(event) {
      console.log("delete this device");
      event.preventDefault();
      var self = this;
      let apiInstance = new Client.DevicesApi();
      apiInstance.devicesImeiDelete(this.$route.params.id);
    },

    /**
     * Collects all data of a device and sets
     * the local form model of this component
     */
    getCurrentDeviceData() {
      var self = this;
      let apiInstance = new Client.DevicesApi();
      apiInstance.devicesImeiGet(this.$route.params.id).then(data => {
        self.form.name = data.name;
        self.form.imei = data.imei;
        self.form.deviceTel = data.devicePhoneNumber;
        self.form.pin = localStorage.getItem(`devices/${data.imei}/pin`);
        self.form.image = localStorage.getItem(`devices/${data.imei}/image`);
      });
    }
  },
  mounted: function() {
    this.getCurrentDeviceData();
  }
};
</script>

<style></style>
