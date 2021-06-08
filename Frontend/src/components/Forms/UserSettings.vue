<template>
  <card class="card-user" v-bind="user">
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
          ><b-icon v-on:click="invokeImageFileSelection" icon="pencil"></b-icon
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

    <!--Some Stats Cards-->
    <div class="row">
      <div
        class="col-xl-4 col-md-6"
        v-for="mythieve in mythieves"
        :key="mythieve.id"
      >
        <stats-card>
          <div slot="header">
            <img
              class="avatar border-gray"
              :src="mythieve.bycyleImageUrl"
              alt="..."
            />
          </div>
          <div slot="content">
            <p class="card-category">Name:</p>
            <h4 class="card-title">{{ mythieve.name }}</h4>
            <p class="card-category">Bikes number:</p>
            <h4 class="card-title">{{ mythieve.deviceTel }}</h4>
            <p class="card-category">Bikes IMEI:</p>
            <h4 class="card-title">{{ mythieve.imei }}</h4>
          </div>
          <div slot="footer">
            <b-button
              ><i class="fa fa-cogs text-warning"></i> {{ mythieve.name }}'s
              Settings</b-button
            >
          </div>
        </stats-card>
      </div>
    </div>

    <div slot="footer" class="text-center d-flex justify-content-center">
      <button href="#" class="btn btn-simple">
        <i class="fa fa-facebook-square"></i>
      </button>
      <button href="#" class="btn btn-simple">
        <i class="fa fa-twitter"></i>
      </button>
      <button href="#" class="btn btn-simple">
        <i class="fa fa-google-plus-square"></i>
      </button>
    </div>
  </card>
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
.content {
  max-height: 100px;
  min-height: 100px;
}

.card-body {
  min-height: 100px;
}
</style>
