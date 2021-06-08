<template>
  <card class="card-user register-device-container">
    <!--Background Picture-->
    <img
      slot="image"
      src="https://verbraucherfenster.hessen.de/sites/verbraucherfenster.hessen.de/files/styles/article_image/public/AdobeStock_173691120.jpeg?itok=w0s4Prt4&c=a03f68c192f0719dbcd708609666a0ea"
      alt="..."
    />
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
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

      <!--Tel-->
      <b-form-group
        id="input-group-3"
        label="Your Telephonenumber:"
        label-for="input-3"
        description="Without your number, My Thieve cannot send you SMS's in case when it cannot send data to Server!"
      >
        <b-form-input
          id="input-3"
          v-model="form.userTel"
          placeholder="Enter Your Telephonebumer: +49..."
          type="tel"
          pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
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
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </card>
</template>

<script>
import { saveAs } from "file-saver";

export default {
  name: "register-device-card",
  components: {},
  data() {
    return {
      form: {
        name: "",
        imei: "",
        userTel: "",
        deviceTel: "",
        pin: "",
        apn: "",
      },
      show: true,
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      //alert(JSON.stringify(this.form));
      this.createConfigFile();
    },
    onReset(event) {
      event.preventDefault();

      // Reset our form values
      this.form.name = "";
      this.form.imei = "";
      this.form.pin = "";
      this.form.userTel = "";
      this.form.deviceTel = "";

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    createConfigFile() {
      var data = `
      #define APN      "${this.form.name}"
      #define IMEI     "${this.form.imei}"
      #define PIN      {'${this.form.pin[0]}','${this.form.pin[1]}','${this.form.pin[2]}','${this.form.pin[3]}'}
      #define PHONE    ${this.form.userTel}"
      #define MYPHONE  ${this.form.deviceTel}"
      #define URL      "TODO"
      #define PASSWORD "TODO"
      #define USER     "TODO"
      `;

      var file = new File([data], "config.h", {
        type: "text/plain;charset=utf-8",
      });

      saveAs(file);
    },
  },
  props: {
    title: {
      type: String,
      description: 'Register new "My Thief" - Device',
    },
    subTitle: {
      type: String,
      description:
        'This Form will create a inital Config-File to setup your "My-Thief"-Device',
    },
    type: {
      type: String,
      description: "primary",
    },
    headerClasses: {
      type: [String, Object, Array],
      description: "Card header css classes",
    },
    bodyClasses: {
      type: [String, Object, Array],
      description: "Card body css classes",
    },
    footerClasses: {
      type: [String, Object, Array],
      description: "Card footer css classes",
    },
  },
};
</script>

<style>
.register-device-container {
  display: flex;
  justify-content: center;
  max-width: 400px;
}
</style>
