<template>
  <b-navbar toggleable="lg" type="dark" variant="dark" sticky>
    <!-- Right aligned nav items -->
    <b-navbar-nav>
      <b-nav-item @click="$router.go(-1)">
        <b-button>
          <i class="fa fa-long-arrow-left"></i>
        </b-button>
      </b-nav-item>
    </b-navbar-nav>
    <b-navbar-brand>Where's my Thief!?</b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item to="/devices/register">
          <b-button block to="">
            <i class="fa fa-plus"></i>
            Register new My Thief
          </b-button>
        </b-nav-item>
        <b-nav-item @click="logout">
          <b-button block>
            <i class="fa fa-sign-out"></i>
            Logout
          </b-button>
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  methods: {
    /**
     *
     */
    logout() {
      var apiInstance = new Client.UsersApi();

      apiInstance
        .usersLogoutPost()
        .then(() => {
          localStorage.removeItem("username");
          localStorage.removeItem("deviceIDs");
          localStorage.removeItem("userPhoneNumber");
          localStorage.removeItem("phonenumber");
          this.$router.push(`/users/login`);
        })
        .catch((a) => {
          console.log("Failed");
        });
    },
  },
};
</script>

<style>
</style>
