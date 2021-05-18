<template>
  <div class="container-fluid">
    <!--Simple Map-->
    <div class="row">
      <div class="col-md-12">
        <MapCard>
          <template slot="header">
            <h4 class="card-title">Bike Live Tracker</h4>
          </template>
        </MapCard>
      </div>
    </div>

    <!--User Information-->
    <card class="card-user" v-bind="mythieve">
      <!--Device Information-->
      <div class="author">
        <!--Device Image-->
        <b-avatar
          badge-variant="light"
          size="7rem"
          :src="mythieve.bycyleImageUrl"
        >
        </b-avatar>

        <!--Device Image-->
        <b-avatar
          badge-variant="light"
          size="7rem"
          :src="mythieve.bycyleImageUrl"
        >
          <div class="battery">
            <div class="battery-level" style="height: 50%">50%</div>
          </div>
        </b-avatar>

        <h4 class="title">
          {{ mythieve.name }}<br />
          <small>Tel: {{ mythieve.deviceTel }}</small
          ><br />
          <small>IMEI: {{ mythieve.imei }}</small
          ><br />
        </h4>
      </div>

      <!--Quote of the Day-->
      <p class="description text-center">
        {{ mythieve.qod }}
      </p>

      <div class="row">
        <div class="col-md-4">
          <router-link :to="'/mythieves/123'">
            Settings<i class="fa fa-cogs text-warning"></i>
          </router-link>
        </div>
      </div>
    </card>
  </div>
</template>

<script>
import StatsCard from "src/components/Cards/StatsCard.vue";
import MapCard from "src/components/Maps/MapCard.vue";

export default {
  name: "device-overview",
  components: {
    StatsCard,
    MapCard,
  },
  data() {
    return {
      mythieve: {
        name: "Bike #1",
        deviceTel: "+49123123123123",
        imei: "492178492440648",
        bycyleImageUrl: "img/bicycles/b-1.jpg",
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

    //UI-Stuff
    goToDeviceSettings() {
      this.setQuoteOfTheUpdate();
    },

    //Fun-Stuff fetching fun things like quates
    setQuoteOfTheUpdate() {
      const self = this;
      fetch("https://api.quotable.io/random")
        .then((response) => response.json())
        .then((data) => (self.mythieve.qod = data.content));
    },
  },
  mounted: function () {
    this.setQuoteOfTheUpdate();
  },
};
</script>

<style lang="scss">
$lightning-size: 18px;

.battery {
  border: 3px solid #333;
  width: 18px;
  height: 28px;
  padding: 2px;
  border-radius: 4px;
  margin: 15px 0;

  &:before {
    content: "";
    height: 3px;
    width: 18px;
    background: #333;
    display: block;
    position: absolute;
    top: -6px;
    border-radius: 4px 4px 0 0;
  }

  &:after {
    content: "";
    display: block;
    position: absolute;
    top: -1px;
    left: -1px;
    right: -1px;
    bottom: -1px;
    border: 1px solid #fff;
    border-radius: 2px;
  }
}

.battery-level {
  background: #30b455;
  position: absolute;
  bottom: 0px;
  left: 0;
  right: 0;

  &.warn {
    background-color: #efaf13;
  }

  &.alert {
    background-color: #e81309;

    &:before {
      background-image: url("data:image/svg+xml;charset=US-ASCII,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22utf-8%22%3F%3E%3C!DOCTYPE%20svg%20PUBLIC%20%22-%2F%2FW3C%2F%2FDTD%20SVG%201.1%2F%2FEN%22%20%22http%3A%2F%2Fwww.w3.org%2FGraphics%2FSVG%2F1.1%2FDTD%2Fsvg11.dtd%22%3E%3Csvg%20version%3D%221.1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20width%3D%2232%22%20height%3D%2232%22%20viewBox%3D%220%200%2032%2032%22%3E%3Cg%3E%3C%2Fg%3E%20%3Cpath%20fill%3D%22%23e81309%22%20d%3D%22M17.927%2012l2.68-10.28c0.040-0.126%200.060-0.261%200.060-0.4%200-0.726-0.587-1.32-1.314-1.32-0.413%200-0.78%200.187-1.019%200.487l-13.38%2017.353c-0.18%200.227-0.287%200.513-0.287%200.827%200%200.733%200.6%201.333%201.333%201.333h8.073l-2.68%2010.28c-0.041%200.127-0.060%200.261-0.060%200.4%200.001%200.727%200.587%201.32%201.314%201.32%200.413%200%200.78-0.186%201.020-0.487l13.379-17.353c0.181-0.227%200.287-0.513%200.287-0.827%200-0.733-0.6-1.333-1.333-1.333h-8.073z%22%3E%3C%2Fpath%3E%3C%2Fsvg%3E");
      background-repeat: no-repeat;
      background-size: $lightning-size;
      height: $lightning-size;
      width: $lightning-size;
      margin: -25px 0 0 2px;
      content: "";
      display: inline-block;
      position: absolute;
    }
  }
}
</style>
