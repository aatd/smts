<template>
  <div class="container-fluid">
    <!--User Information-->
    <card class="card-user" v-bind="user">
      <!--Background Picture-->
      <img slot="image" :src="user.bgImg" alt="..." />

      <!--User Information-->
      <div class="author">
        <b-avatar badge-variant="light" size="7rem" :src="user.image">
        </b-avatar>

        <h4 class="title">
          {{ user.name }}<br />
          <small>{{ user.email }}</small>
        </h4>
      </div>

      <!--Quote of the Day-->
      <p class="description text-center">
        {{ user.qod }}
      </p>

      <div class="row justify-content-center">
        <b-button pill><b-icon icon="pencil"></b-icon></b-button>
      </div>
    </card>

    <!--Cards for each Device-->
    <div class="row">
      <div
        class="col-xl-6 col-md-8"
        v-for="mythieve in mythieves"
        :key="mythieve.id"
      >
        <stats-card>
          <div slot="header">
            <b-avatar size="100" :src="mythieve.bycyleImageUrl"> </b-avatar>
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
          <div slot="footer">
            <div @click="setQuoteOfTheUpdate">
              <router-link :to="'/mythieves/123'">
                Settings<i class="fa fa-cogs text-warning"></i>
              </router-link>
            </div>
          </div>
        </stats-card>
      </div>
    </div>
  </div>
</template>

<script>
import StatsCard from "src/components/Cards/StatsCard.vue";

export default {
  name: "user-overview",
  components: {
    StatsCard,
  },
  data() {
    return {
      user: {
        name: "Asef Alper Tunga Dündar",
        email: "asaf93@hotmail.de",
        tel: "+490123456789",
        image: "img/faces/face-2.jpg",
        bgImg: "img/bicycles/b-7.jpg",
        qod: "Test an api for Fun-Attribute",
      },
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
        {
          name: "Bike #5",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-4.jpg",
        },
        {
          name: "Bike #6",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-4.jpg",
        },
        {
          name: "Bike #7",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-4.jpg",
        },
        {
          name: "Bike #8",
          deviceTel: "+49123123123123",
          imei: "492178492440648",
          bycyleImageUrl: "img/bicycles/b-4.jpg",
        },
      ],
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

    //UI-Stuff
    goToDeviceSettings() {
      this.setQuoteOfTheUpdate();
    },

    //Fun-Stuff fetching fun things like quates
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
</style>
