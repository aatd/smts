<template>
  <div class="container-fluid">
    <card class="card-user devices-container" v-bind="form">
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
          id="input-group-1"
          label="Device Name:"
          label-for="input-1"
          description='Choose a Name of your "My Thief"-Device!'
        >
          <b-form-input
            id="input-1"
            v-model="form.name"
            placeholder="Enter a cool Name..."
            required
          ></b-form-input>
        </b-form-group>

        <!--IMEI-->
        <b-form-group
          id="input-group-2"
          label="IMEI:"
          label-for="input-2"
          description="On your SIM-Card you will find your IMEI Number. Withour that number the My-Thieve cannot dial in to the Web!"
        >
          <b-form-input
            id="input-2"
            v-model="form.imei"
            placeholder="Enter IMEI..."
            type="tel"
            required
          ></b-form-input>
        </b-form-group>

        <!--Device-Tel-->
        <b-form-group
          id="input-group-3"
          label="My-Thieves Telephonenumber:"
          label-for="input-4"
          description="The number of your My-Thieves SIM-Card. If you want to send SMS's to configure your My-Thieve"
        >
          <b-form-input
            id="input-4"
            v-model="form.deviceTel"
            placeholder="Enter Telnnumber: +49..."
            type="tel"
            required
          ></b-form-input>
        </b-form-group>

        <!--SIM-PIN-->
        <b-form-group
          id="input-group-4"
          label="My-Thieves SIM-PIN:"
          label-for="input-5"
          description="To activate your SIM-Card we need it's PIN in it's Configuration."
        >
          <b-form-input
            id="input-5"
            v-model="form.pin"
            placeholder="XXXX"
            type="tel"
            size="4"
            maxlength="4"
            required
          ></b-form-input>
        </b-form-group>

        <!--Submit Button-->
        <b-button block type="submit" variant="primary">Save changes</b-button>
      </b-form>

      <!--Debug Stuff-->
      <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
        <pre class="m-0">{{ form }}</pre>
        <b-button @click="onReset" block variant="danger">Reset</b-button>
      </b-card>
    </card>
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
      },
    };
  },
  methods: {
    /**
     *
     */
    onReset() {
      // Reset our form values
      this.form.name = "";
      this.form.imei = "";
      this.form.pin = "";
      this.form.deviceTel = "";

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },

    /**
     *
     */
    invokeImageFileSelection() {
      document.getElementById("imgDeviceFile").click();
    },

    /**
     *
     */
    onChangeDeviceImage(event) {
      var self = this;
      const image = event.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = (event) => {
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
     *
     */
    onUpdateDeviceSetings(event) {
      event.preventDefault();
    },

    /**
     *
     */
    getCurrentDeviceData() {
      var self = this;
      let apiInstance = new Client.DevicesApi();
      apiInstance.devicesImeiGet(this.$route.params.id).then((data) => {
        self.form.name = data.name;
        self.form.imei = data.imei;
        self.form.deviceTel = data.devicePhoneNumber;
        self.form.pin = localStorage.getItem(`devices/${data.imei}/pin`);
        self.form.image = localStorage.getItem(`devices/${data.imei}/image`);
      });
    },
  },
  mounted: function () {
    this.getCurrentDeviceData();
  },
};
</script>

<style>
</style>
