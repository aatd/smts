<template>
  <card class="card-user" v-bind="user">
    
    <!--Background Picture-->
    <img
      slot="image"
      :src="user.bgImg"
      alt="..."
    />

    <!--User Information-->
    <div class="author">
      <img class="avatar border-gray" :src="user.image" alt="..." />
      <h4 class="title">
        {{user.name}}<br />
        <small>{{user.email}}</small>
      </h4>
    </div>

    <!--Quote of the Day-->
    <p class="description text-center">
      {{user.qod}}
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
            <b-button><i class="fa fa-cogs text-warning"></i> {{mythieve.name}}'s Settings</b-button>
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
import StatsCard from "src/components/Cards/StatsCard.vue";

export default {
  name: "user-profile",
  components: {
    Card,
    StatsCard,
  },
  data() {
    return {
      data: {},
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
      details: [
        {
          title: "12",
          subTitle: "Files",
        },
        {
          title: "2GB",
          subTitle: "Used",
        },
        {
          title: "24,6$",
          subTitle: "Spent",
        },
      ],
      user:{
        name:  "Asef Alper Tunga Dündar",
        email: "asaf93@hotmail.de",
        tel:   "+490123456789",
        image: "img/faces/face-2.jpg",
        bgImg: "img/bicycles/b-7.jpg",
        qod:   "Test an api for Fun-Attribute",
      }
    };
  },
  methods: {
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
  },
  mounted: function () {
    const self = this;
    fetch('https://api.quotable.io/random')
      .then(response => response.json())
      .then(data => self.user.qod = data.content)
      .then(data => console.log(data));
  },
};
</script>

<style>
.content{
  max-height: 100px;
  min-height: 100px;
}

.card-body{
  min-height: 100px;
}
</style>