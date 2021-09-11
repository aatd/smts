<template>
  <div class="container-fluid">
    <!--Page Content-->
    <card class="where-is-my-thief-container-avatar card-user" v-bind="user">
      <!--User Information-->
      <div class="author">
        <b-avatar badge-variant="light" size="7rem" :src="user.image">
        </b-avatar>

        <h4 class="title">
          {{ user.name }}<br />
          <small>{{ user.tel }}</small>
        </h4>
      </div>

      <!--Quote of the Day-->
      <p class="description text-center">
        {{ user.qod }}
      </p>

      <div class="m-2 row">
        <b-button block pill :to="`/users/${$route.params.id}/settings`">
          Edit Profile<b-icon icon="pencil"> </b-icon>
        </b-button>
      </div>
      <div class="row device-card-list">
        <div class="col-xl-12" v-for="mythieve in mythieves" :key="mythieve.id">
          <router-link :to="`/devices/${mythieve.imei}`">
            <stats-card>
              <div slot="header">
                <b-avatar
                  size="100"
                  icon="bicycle"
                  :src="mythieve.deviceImage"
                ></b-avatar>
              </div>
              <div slot="content">
                <p class="card-category">Name:</p>
                <h4 class="card-title">
                  {{ mythieve.name }}
                </h4>
                <p class="card-category">Bikes number:</p>
                <h4 class="card-title">
                  <small>{{ mythieve.deviceTel }}</small>
                </h4>
              </div>
            </stats-card>
          </router-link>
        </div>
      </div>
    </card>
  </div>
</template>

<script>
import StatsCard from "../components/Cards/StatsCard.vue";
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  name: "user-overview-page",
  components: {
    StatsCard
  },
  data() {
    return {
      user: {
        name: "",
        email: "",
        tel: "",
        image: "",
        qod: ""
      },
      mythieves: []
    };
  },
  methods: {
    /**
     *
     */
    setQuoteOfTheUpdate() {
      const self = this;
      fetch("https://api.quotable.io/random")
        .then(response => response.json())
        .then(data => (self.user.qod = data.content));
    },

    /**
     *
     */
    getUserData() {
      var apiInstance = new Client.UsersApi();
      apiInstance
        .getUserbyId(localStorage.getItem("id"))
        .then(data => {
          console.log(
            "Got userdata succesfully to fill userinformation to overview page"
          );
          localStorage.setItem("username", data.name);
          this.user.name = data.name;
          localStorage.setItem("phonenumber", data.phoneNumber);
          this.user.tel = data.phoneNumber;
          localStorage.setItem("deviceids", JSON.stringify(data.devices));
          this.user.image = localStorage.getItem(`users/${data.name}/image`);
        })
        .catch(error => {
          if (error.response.status == 401) {
            console.log(error.response.text);
            this.$bvToast.show("login-error-credentials-toast");
          } else {
            this.$bvToast.show("login-error-server-toast");
          }
        });
    },

    /**
     *
     */
    getDevices() {
      var apiInstance = new Client.UsersApi();
      var username = localStorage.getItem("username");

      apiInstance.findAllDevices(localStorage.getItem("id")).then(data => {
        console.log("Got Device Object");
        data.forEach(device => {
          this.mythieves.push({
            name: device.name,
            deviceTel: device.devicePhoneNumber,
            imei: device.imei,
            deviceImage: localStorage.getItem(`devices/${device.imei}/image`)
          });
        });
      });
    }
  },
  mounted: function() {
    this.setQuoteOfTheUpdate();
    this.getUserData();
    this.getDevices();
  }
};
</script>

<style>
.device-card-list {
  justify-content: center;
}

.devices-container {
  max-width: 400px;
  margin: auto;
  margin-top: 120px;
}
</style>
