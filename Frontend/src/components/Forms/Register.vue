<template>
  <card class="card-user register-container">
    <!--Background Picture-->
    <img
      slot="image"
      src="https://verbraucherfenster.hessen.de/sites/verbraucherfenster.hessen.de/files/styles/article_image/public/AdobeStock_173691120.jpeg?itok=w0s4Prt4&c=a03f68c192f0719dbcd708609666a0ea"
      alt="..."
    />
    <b-form @submit="onRegister" @reset="onReset" v-if="show">
      <!--Username-->
      <b-form-group
        id="input-group-1"
        label="Create a username:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.username"
          placeholder="Enter your Personal Username"
          required
        ></b-form-input>
      </b-form-group>

      <!--Email-->
      <b-form-group
        id="input-group-2"
        label="Email address:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>

      <!--Telephone-->
      <b-form-group
        id="input-group-2"
        label="Telephone Number:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.tel"
          type="tel"
          placeholder="Enter your Mobilephone Number"
          required
        ></b-form-input>
      </b-form-group>

      <!--Password-->
      <b-form-group
        id="input-group-3"
        label="Your Password:"
        label-for="input-3"
      >
        <b-form-input
          id="input-3"
          v-model="form.pwd"
          type="password"
          placeholder="Enter a Password"
          required
        ></b-form-input>
      </b-form-group>

      <!--Password Check-->
      <b-form-group
        id="input-group-4"
        label="Your Password again:"
        label-for="input-4"
      >
        <b-form-input
          id="input-4"
          v-model="form.pwdCheck"
          type="password"
          placeholder="Re-enter Password"
          required
        ></b-form-input>
      </b-form-group>

      <!--Submit Button-->
      <b-button block type="submit" variant="primary">Register</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
      <pre class="m-0">{{ form }}</pre>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-card>
  </card>
</template>

<script>
export default {
  name: "register-card",
  components: {},
  data() {
    return {
      form: {
        username: "",
        email: "",
        tel: "",
        pwd: "",
        pwdCheck: "",
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
      this.form.email = "";
      this.form.username = "";
      this.form.pwd = "";
      this.form.pwdCheck = "";

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onRegister(event) {
      this.$router.push("/users/1234");
    },
  },
};
</script>

<style>
.register-container {
  display: flex;
  justify-content: center;
  max-width: 400px;
}
</style>
