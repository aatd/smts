<template>
  <div class="content">
    <div class="container-fluid">
      <!--Page Content-->
      <card class="card-user where-is-my-thief-container">
        <!--Background Picture-->
        <img slot="image" src="img/logo.png" alt="..." />

        <!--Login Form-->
        <b-form @submit="onLogin">
          <!--Email or Name-->
          <b-form-group
            id="input-group-login-name"
            label="Email address or Username:"
            label-for="input-login-name"
            description="We'll never share this information with anyone else."
          >
            <b-form-input
              id="input-login-name"
              v-model="form.name"
              placeholder="Enter email or username"
              required
            ></b-form-input>
          </b-form-group>

          <!--Password-->
          <b-form-group
            id="input-group-login-password"
            label="Your Password:"
            label-for="input-login-password"
          >
            <b-form-input
              id="input-login-password"
              type="password"
              v-model="form.pwd"
              placeholder="Enter Password"
              required
            ></b-form-input>
          </b-form-group>

          <!--Remeber me-->
          <b-form-group
            id="input-group-login-remeber-me"
            label-for="input-login-remeber-me"
          >
            <b-form-checkbox-group
              v-model="form.checked"
              id="input-login-remeber-me"
            >
              <b-form-checkbox value="rememberMe">Remeber me</b-form-checkbox>
            </b-form-checkbox-group>
            <router-link to="/users/register">Not registered yet?</router-link>
          </b-form-group>

          <!--Submission Button-->
          <b-button block type="submit" variant="primary">Login</b-button>
        </b-form>

        <!--Debug Stuff-->
        <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
          <pre class="m-0">{{ form }}</pre>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-card>
      </card>
    </div>

    <!--Toast collection for this Component/Page-->
    <div id="login-toasts">
      <!--Toast generic login error-->
      <b-toast
        id="login-error-toast"
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
        Your credentails may be wrong or you didn't start the Where's my Thief
        Server
      </b-toast>

      <!--Toast Credentails error-->
      <b-toast
        id="login-error-credentials-toast"
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
        Your credentails are wrong!
      </b-toast>

      <!--Toast Server error-->
      <b-toast
        id="login-error-server-toast"
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
        Login failed due server error. Is the Server running?
      </b-toast>
    </div>
  </div>
</template>

<script>
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  name: "login-page",
  data() {
    return {
      form: {
        name: "",
        pwd: "",
        checked: [],
      },
    };
  },
  methods: {
    /**
     *
     */
    onLogin(event) {
      event.preventDefault();

      var userModel = new Client.User();
      userModel.name = this.form.name;
      userModel.password = this.form.pwd;

      var apiInstance = new Client.UsersApi();

      apiInstance
        .loginUser({ user: userModel })
        .then((data) => {
          console.log("Login successeded");
          localStorage.setItem("username", data.name);
          localStorage.setItem("phonenumber", data.phoneNumber);
          this.$router.push(`/users/${data.name}`);
        })
        .catch((error) => {
          if (error.response.status == 401) {
            console.log(error.response.text);
            this.$bvToast.show("login-error-credentials-toast");
          } else {
            this.$bvToast.show("login-error-server-toast");
          }
        });
    },
    /**
     * Debug only, resets the json Object which wold be sended to server
     */
    onReset() {
      // Reset our form values
      this.form.name = "";
      this.form.pwd = "";
      this.form.checked = [];

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style>
</style>
