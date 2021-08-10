<template>
  <div class="container-fluid">
    <card class="card-user update-userdata-container" v-bind="user">
      <!--Background Picture-->
      <img
        slot="image"
        :src="user.bgImg"
        alt="..."
        v-on:click="invokeBGImageFileSelection"
      />

      <!--User Information-->
      <div class="author">
        <b-avatar badge-variant="info" size="150" :src="user.image">
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
          id="imgFile"
          accept="image/jpeg, image/png"
          @change="onchangeProfileImage"
        ></b-form-file>

        <!-- Accept specific image formats by IANA type -->
        <b-form-file
          v-show="false"
          id="bgImgFile"
          accept="image/jpeg, image/png"
          @change="onChangeBGImage"
        ></b-form-file>

        <h4 class="title">
          {{ user.name }}<br />
          <small>{{ user.email }}</small>
        </h4>
      </div>

      <!--Quote of the Day-->
      <p class="description text-center">
        {{ user.qod }}
      </p>

      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <!--Username-->
        <b-form-group
          id="change-username-input-group"
          label="Change username:"
          label-for="change-username-input"
        >
          <b-form-input
            id="change-username-input"
            v-model="form.username"
            placeholder="Enter a new Username here"
          ></b-form-input>
        </b-form-group>

        <!--Email-->
        <b-form-group
          id="change-email-input-group"
          label="Email address:"
          label-for="change-email-input"
        >
          <b-form-input
            id="change-email-input"
            v-model="form.email"
            type="email"
            placeholder="Enter email"
          ></b-form-input>
        </b-form-group>

        <!--Tel-->
        <b-form-group
          id="change-tel-input-group"
          label="Telephone Number:"
          label-for="change-email-input"
        >
          <b-form-input
            id="change-email-input"
            v-model="form.email"
            type="tel"
            placeholder="Enter Telephone number"
          ></b-form-input>
        </b-form-group>

        <!--Current Password-->
        <b-form-group
          id="change-password-old-input-group"
          label="Your current Password:"
          label-for="change-password-old-input"
        >
          <b-form-input
            id="change-password-old-input"
            v-model="form.pwd"
            type="password"
            placeholder="Enter your current Password"
            required
          ></b-form-input>
        </b-form-group>

        <!--New Password-->
        <b-form-group
          id="input-group-4"
          label="Your new Password:"
          label-for="input-4"
        >
          <b-form-input
            id="change-password-new-input"
            v-model="form.pwdCheck"
            type="password"
            placeholder="Enter a new Password"
          ></b-form-input>
        </b-form-group>

        <!--New Password Check-->
        <b-form-group
          id="input-group-4"
          label="Your new Password again:"
          label-for="input-4"
        >
          <b-form-input
            id="change-password-new-input"
            v-model="form.pwdCheck"
            type="password"
            placeholder="Re-enter your new Password"
          ></b-form-input>
        </b-form-group>

        <!--Submit Button-->
        <b-button block type="submit" variant="primary">Save changes</b-button>
      </b-form>
      <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
        <pre class="m-0">{{ form }}</pre>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-card>
    </card>
  </div>
</template>

<script>
import Card from "src/components/Cards/Card.vue";

export default {
  name: "user-profile",
  components: {
    Card,
  },
  data() {
    return {
      mythieves: [
        {
          name: "Bike #1",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-1.jpg",
        },
        {
          name: "Bike #2",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-2.jpg",
        },
        {
          name: "Bike #3",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-3.jpg",
        },
        {
          name: "Bike #4",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-4.jpg",
        },
      ],
      user: {
        name: "Asef Alper Tunga Dündar",
        email: "asaf93@hotmail.de",
        tel: "+490123456789",
        image: "img/faces/face-2.jpg",
        bgImg: "img/bicycles/b-7.jpg",
        qod: "Test an api for Fun-Attribute",
      },
      form: {
        username: "",
        email: "",
        pwdOld: "",
        pwdNew: "",
        pwdNewCheck: "",
      },
      show: true,
    };
  },
  methods: {
    //Design Stuff
    getClasses(index) {
      var remainder = index % 3;
      if (remainder === 0) {
        return "col-md-3 col-md-offset-1";
      } else if (remainder === 2) {
        return "col-md-4";
      } else {
        return "col-md-3";
      }
    },

    //Debug Stuff
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

    //Sending Stuff
    updateProfileImage() {
      console.log("Not Implemented");
    },
    updateBGImage() {
      console.log("Not Implemented");
    },
    updateProfileSettings() {
      console.log("Not Implemented");
    },

    //UI-Stuff for Images
    invokeBGImageFileSelection() {
      document.getElementById("bgImgFile").click();
    },
    invokeImageFileSelection() {
      document.getElementById("imgFile").click();
    },
    onchangeProfileImage(e) {
      self = this;
      const image = e.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = (e) => {
        this.previewImage = e.target.result;
        self.user.image = e.target.result;
      };
    },
    onChangeBGImage(e) {
      self = this;
      const image = e.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = (e) => {
        this.previewImage = e.target.result;
        self.user.bgImg = e.target.result;
      };
    },

    //Fun-Stuff fetching fun things like quoates
    setQuoteOfTheUpdate() {
      const self = this;
      fetch("https://api.quotable.io/random")
        .then((response) => response.json())
        .then((data) => (self.user.qod = data.content));
    },
  },
  mounted: function () {
    this.setQuoteOfTheUpdate();
  },
};
</script>

<style>
.update-userdata-container {
  display: flex;
  justify-content: center;
  margin: auto;
  margin-top: 15px;
  max-width: 400px;
}
</style>
