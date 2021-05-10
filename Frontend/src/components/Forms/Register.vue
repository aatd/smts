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
  name: "register-card",
  components: {},
  data() {
    return {
      form: {
        username: "",
        email: "",
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
      this.form.email    = "";
      this.form.username = "";
      this.form.pwd      = "";
      this.form.pwdCheck = "";

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick( () => {this.show = true;} );

    },
  },
  props: {
    title: {
      type: String,
      description: "Register",
    },
    subTitle: {
      type: String,
      description:
        "Some information about you so you can set up your Bikes in the next step!",
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
