<template>
  <div class="card" :class="[type && `card-${type}`]">
    <div class="card-image" v-if="$slots.image">
      <slot name="image"></slot>
    </div>
    <div
      class="card-header"
      v-if="$slots.header || title"
      :class="headerClasses"
    >
      <slot name="header">
        <h4 class="card-title">{{ title }}</h4>
      </slot>
      <p class="card-category" v-if="subTitle">{{ subTitle }}</p>
    </div>
    <div class="card-body">
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
      <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
    </div>
    <slot name="raw-content"></slot>
    <div class="card-footer" :class="footerClasses" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
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
      },
      show: true,
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      alert(JSON.stringify(this.form));
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
</style>