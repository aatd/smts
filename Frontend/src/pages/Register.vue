<template>
  <div class="content">
    <div class="container-fluid">
      <card class="card-user register-container">
        <!--Background Picture-->
        <img slot="image" src="img/logo.png" alt="..." />
        <b-form @submit="onRegister">
          <!--Username-->
          <b-form-group
            id="input-group-register-name"
            label="Create a username:"
            label-for="input-register-name"
          >
            <b-form-input
              id="input-register-name"
              v-model="form.name"
              placeholder="Enter your personal Username"
              required
            ></b-form-input>
          </b-form-group>

          <!--Telephone-->
          <b-form-group
            id="input-group-register-telnumber"
            label="Telephone Number:"
            label-for="input-register-telnumber"
          >
            <b-form-input
              id="input-group-register-telnumber"
              v-model="form.tel"
              type="tel"
              placeholder="Enter your Mobilephone Number"
              required
            ></b-form-input>
          </b-form-group>

          <!--Password-->
          <b-form-group
            id="input-group-register-password"
            label="Your Password:"
            label-for="input-register-password"
          >
            <b-form-input
              id="input-register-password"
              v-model="form.pwd"
              type="password"
              placeholder="Enter a Password"
              required
            ></b-form-input>
          </b-form-group>

          <!--Password Check-->
          <b-form-group
            id="input-group-register-password-check"
            label="Your Password again:"
            label-for="input-register-password-check"
          >
            <b-form-input
              id="input-register-password-check"
              v-model="form.pwdCheck"
              type="password"
              placeholder="Re-enter Password"
              required
            ></b-form-input>
          </b-form-group>

          <!--Submit Button-->
          <b-button block type="submit" variant="primary"> Register </b-button>

          <!--Go back to Login-Button-->
          <b-button block variant="primary" to="/users/login">
            Already an account? Login!
          </b-button>
        </b-form>
        <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
          <pre class="m-0">{{ form }}</pre>
          <b-button block @click="onReset" variant="danger">Reset</b-button>
        </b-card>
      </card>
    </div>
  </div>
</template>

<script>
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  name: "register-card",
  components: {},
  data() {
    return {
      form: {
        username: "",
        tel: "",
        pwd: "",
        pwdCheck: "",
      },
    };
  },
  methods: {
    /**
     *
     */
    onReset() {
      // Reset our form values
      this.form.tel = "";
      this.form.username = "";
      this.form.pwd = "";
      this.form.pwdCheck = "";

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },

    /**
     *
     */
    onRegister(event) {
      event.preventDefault();
      var apiInstance = new Client.UsersApi();

      // Create User model for API-Call
      var userModel = new Client.User();
      userModel.name = this.form.name;
      userModel.password = this.form.pwd;
      userModel.phoneNumber = this.form.tel;

      // Create User on Server
      apiInstance
        .createUser(userModel)
        .then((data) => {
          console.log("Registration successeded.");
          this.$router.push(`/users/${data.name}`);
        })
        .catch(() => {
          console.log("Registration failed");
        });
    },
  },
};
</script>

<style>
.register-container {
  max-width: 400px;
}
</style>
