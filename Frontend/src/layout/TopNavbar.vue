<template>
  <b-navbar toggleable="lg" type="dark" variant="dark" sticky>
    <!-- Right aligned nav items -->
    <b-navbar-nav>
      <b-nav-item @click="goBack">
        <b-button v-if="showGoBackButton">
          <i class="fa fa-long-arrow-left"></i>
        </b-button>
      </b-nav-item>
    </b-navbar-nav>
    <b-navbar-brand
      >Where's my Thief!?
      <a href="https://github.com/aatd/smts">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-github"
          viewBox="0 0 16 16"
        >
          <path
            d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"
          /></svg
      ></a>
    </b-navbar-brand>
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
  data() {
    return {
      showGoBackButton: true,
    };
  },
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
    goBack() {
      if (this.$router.currentRoute.name != "UserOverview") {
        this.$router.go(-1);
      }
    },
  },
  watch: {
    $route(to, from) {
      if (to.name === "UserOverview") {
        this.showGoBackButton = false;
      } else {
        this.showGoBackButton = true;
      }
    },
  },
};
</script>

<style></style>
