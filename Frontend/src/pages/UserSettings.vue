<template>
  <div class="container-fluid">
    <!--Page Content-->
    <card class="card-user where-is-my-thief-container-avatar" v-bind="form">
      <!--Profile image which is just sotred locally for ecological reasons-->
      <div id="changeImageForm" class="author">
        <b-avatar badge-variant="info" size="7rem" :src="form.image">
          <template #badge
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
          @change="onChangeProfileImage"
        ></b-form-file>
      </div>

      <!--Actucal important data which are goiing to be changed-->
      <b-form id="changeProfileSettingsForm" @submit="updateProfileSettings">
        <!--Username-->
        <b-form-group
          id="input-group-update-user-name"
          label="Change username:"
          label-for="input-update-user-name"
        >
          <b-form-input
            id="input-update-user-name"
            v-model="form.username"
            placeholder="Enter a new Username here"
          ></b-form-input>
        </b-form-group>

        <!--Tel-->
        <b-form-group
          id="input-group-update-user-tel"
          label="Telephone Number:"
          label-for="input-update-user-tel"
        >
          <b-form-input
            id="input-update-user-tel"
            v-model="form.tel"
            type="tel"
            placeholder="Enter Telephone number"
          ></b-form-input>
        </b-form-group>

        <!--Current Password-->
        <b-form-group
          id="input-group-update-user-pwd"
          label="Your current Password:"
          label-for="input-update-user-pwd"
        >
          <b-form-input
            id="input-update-user-pwd"
            v-model="form.pwdOld"
            type="password"
            placeholder="Enter your current Password"
          ></b-form-input>
        </b-form-group>

        <!--New Password-->
        <b-form-group
          id="input-group-update-user-new-pwd"
          label="Your new Password:"
          label-for="input-update-user-new-pwd"
        >
          <b-form-input
            id="input-update-user-new-pwd"
            v-model="form.pwdNew"
            type="password"
            placeholder="Enter a new Password"
          ></b-form-input>
        </b-form-group>

        <!--New Password Check-->
        <b-form-group
          id="input-group-update-user-new-pwd-check"
          label="Your new Password again:"
          label-for="input-update-user-new-pwd-check"
        >
          <b-form-input
            id="input-update-user-new-pwd-check"
            v-model="form.pwdNewCheck"
            type="password"
            placeholder="Re-enter your new Password"
          ></b-form-input>
        </b-form-group>

        <!--Submit Button-->
        <b-button block type="submit" variant="primary">Save changes</b-button>
        <b-button block v-b-modal.deleteUserModal variant="danger">
          Delete your account
        </b-button>
      </b-form>

      <!--Debug Stuff-->
      <b-card class="mt-3" header="Form Data Result" v-if="$IsDebug">
        <pre class="m-0">{{ form }}</pre>
        <b-button block @click="onReset" variant="danger">Reset</b-button>
      </b-card>
    </card>

    <!--Page Modals-->
    <div class="modals">
      <!--Delete user Modal-->
      <b-modal
        id="deleteUserModal"
        title="Do you really want to delete your Account?"
        hide-footer
        centered="false"
      >
        <!--Download Config file-->
        <b-button class="mt-3" variant="danger" block @click="deleteUser">
          Delete Useraccount and all Devices permanently
        </b-button>

        <!--Close Modal-->
        <b-button class="mt-3" block @click="$bvModal.hide('deleteUserModal')">
          Cancel
        </b-button>
      </b-modal>
    </div>
  </div>
</template>

<script>
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  name: "update-user-page",
  data() {
    return {
      form: {
        username: "",
        tel: "",
        image: "",
        pwdOld: "",
        pwdNew: "",
        pwdNewCheck: ""
      }
    };
  },
  methods: {
    /**
     *
     */
    onReset() {
      // Reset our form values
      this.form.username = "";
      this.form.tel = "";
      this.form.image = "";
      this.form.pwdOld = "";
      this.form.pwdNew = "";
      this.form.pwdNewCheck = "";

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },

    /**
     * Attpemts to update the current user on the server
     */
    updateProfileSettings() {
      var self = this;
      var apiInstance = new Client.UsersApi();
      var userModel = new Client.User();

      //Name
      userModel.name = this.form.username;

      //Phonenumber
      userModel.phoneNumber = this.form.tel;

      //New Password
      if (
        this.form.pwdNew != this.form.pwdNewCheck &&
        this.form.pwdNew != "" &&
        this.form.pwdNewCheck != ""
      ) {
        console.log("New Password not doublechecked.");
        return;
      }
      userModel.password = this.form.pwdNew;

      apiInstance
        .updateUser(localStorage.getItem("id"), {
          user: userModel
        })
        .then(data => {
          // get all old local stuff
          var oldUsername = localStorage.getItem("username");
          var image = localStorage.getItem(`users/${oldUsername}/image`);

          // change all new items
          localStorage.setItem("username", data.name);
          localStorage.setItem("phonenumber", data.phoneNumber);
          localStorage.setItem(`users/${data.name}/image`, image);

          // remove old image
          localStorage.removeItem(`users/${oldUsername}/image`);

          // navigate to overivew
          this.$router.push(`/users/${data.name}`);
          console.log("Successfull updated user");
        })
        .catch(error => {});
    },

    /**
     * Attempts to delete the current user on the server
     */
    deleteUser() {
      var apiInstance = new Client.UsersApi();
      apiInstance.usersUserIdDelete(this.$route.params.id).then;
      this.$router.push(`/users/login`);
    },

    /**
     * Methods invokes the hidden
     * fileselsction element so we
     * can use a generic HTML-Element
     * for fileselection
     */
    invokeImageFileSelection() {
      document.getElementById("imgFile").click();
    },

    /**
     * Callback Method when fileselection
     * for the Porfileimage ws completed.
     * Saves the choosen image to localstorage
     */
    onChangeProfileImage(event) {
      var self = this;
      const image = event.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = event => {
        this.previewImage = event.target.result;
        var username = localStorage.getItem("username");
        localStorage.setItem(`users/${username}/image`, event.target.result);
        self.form.image = localStorage.getItem(`users/${username}/image`);
      };
    },

    /**
     * Collects all data of a user and sets
     * the local form model of this component
     */
    getCurrentUserData() {
      let self = this;
      let apiInstance = new Client.UsersApi();
      let username = localStorage.getItem("username");
      apiInstance.getUserbyId(localStorage.getItem("id")).then(data => {
        console.log(data);
        self.form.username = data.name;
        self.form.tel = data.phoneNumber;
        self.form.image = localStorage.getItem(`users/${username}/image`);
      });
    }
  },
  mounted: function() {
    this.getCurrentUserData();
  }
};
</script>

<style></style>
