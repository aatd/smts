<template>
  <!--User Information-->
  <card class="card-user login-container">
    <!--Background Picture-->
    <img
      slot="image"
      src="https://verbraucherfenster.hessen.de/sites/verbraucherfenster.hessen.de/files/styles/article_image/public/AdobeStock_173691120.jpeg?itok=w0s4Prt4&c=a03f68c192f0719dbcd708609666a0ea"
      alt="..."
    />
    <b-form @submit="onLogin" @reset="onReset" v-if="show">
      <!--Email or Name-->
      <b-form-group
        id="input-group-1"
        label="Email address or Username:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="form.emailOrName"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>

      <!--Password-->
      <b-form-group
        id="input-group-2"
        label="Your Password:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          type="password"
          v-model="form.pwd"
          placeholder="Enter Password"
          required
        ></b-form-input>
      </b-form-group>

      <!--Remeber me-->
      <b-form-group id="input-group-4" v-slot="{ ariaDescribedby }">
        <b-form-checkbox-group
          v-model="form.checked"
          id="checkboxes-4"
          :aria-describedby="ariaDescribedby"
        >
          <b-form-checkbox value="rememberMe">Remeber me</b-form-checkbox>
        </b-form-checkbox-group>
        <router-link to="/users/register">Not registered yet?</router-link>
      </b-form-group>

      <!--Submission Button-->
      <b-button block type="submit" variant="primary">Login</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
      <pre class="m-0">{{ form }}</pre>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-card>
  </card>
</template>

<script>
import Card from "src/components/Cards/Card.vue";
import * as Client from "src/components/api/index";

export default {
  name: "login-card",
  components: {
    Card,
  },
  data() {
    return {
      form: {
        emailOrName: "",
        pwd: "",
        checked: [],
      },
      show: true,
    };
  },
  methods: {
    onLogin(event) {
      event.preventDefault();

      this.$router.push("/users/1234");

      var user2 = new Client.User();
      user2.name = this.form.emailOrName;
      user2.password = this.form.pwd;

      var apiInstance = new Client.UsersApi();

      apiInstance
        .loginUser({ user: user2 })
        .then(() => {
          console.log("Hello");
        })
        .catch((a) => {
          console.log("Failed");
        });
    },
    onSubmit(event) {
      event.preventDefault();
      alert(JSON.stringify(this.form));
    },
    onReset(event) {
      event.preventDefault();

      // Reset our form values
      this.form.emailOrName = "";
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
.login-container {
  max-width: 400px;
}
</style>
