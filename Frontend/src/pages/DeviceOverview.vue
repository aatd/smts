<template>
  <div class="container-fluid">
    <!--User Information-->
    <card class="card-user devices-container" v-bind="mythief">
      <!--Device Information-->
      <div class="author">
        <div>
          <b-avatar
            badge-variant="light"
            size="120px"
            icon="bicycle"
            :src="mythief.image"
          >
          </b-avatar>
          <b-avatar
            badge-variant="light"
            size="70px"
            :src="mythief.bycyleImageUrl"
          >
            <div class="battery">
              <div
                id="battery-indicator"
                class="battery-level"
                style="z-index: -1"
              ></div>
              <small id="battery-label"></small>
            </div>
          </b-avatar>
        </div>

        <h4 class="title">
          {{ mythief.name }}<br />
          <small>Tel: {{ mythief.deviceTel }}</small
          ><br />
          <small>IMEI: {{ mythief.imei }}</small
          ><br />
        </h4>
      </div>
      <h4 class="title">
        Live tracker
        <b-badge v-if="mythief.status == 'active'" variant="danger">
          tracker active
        </b-badge>
        <b-badge v-else-if="mythief.status == 'inactive'" variant="success">
          tracker inactive
        </b-badge>
        <b-badge v-else variant="secondary" pill>status unknown</b-badge>
      </h4>
      <b-button variant="danger" block v-b-modal.callPoliceModal>
        Call Police<b-icon icon="telephone"> </b-icon>
      </b-button>
      <b-form-select
        v-model="timeInterval"
        class="mb-3"
        v-if="mythief.status == 'active'"
      >
        <b-form-select-option value="0">Show recent data</b-form-select-option>
        <b-form-select-option value="10">10min</b-form-select-option>
        <b-form-select-option value="30">30min</b-form-select-option>
        <b-form-select-option value="60">60min</b-form-select-option>
        <b-form-select-option value="120">120min</b-form-select-option>
        <b-form-select-option value="180">180min</b-form-select-option>
      </b-form-select>
      <!--Device Location Map-->
      <MapCard :deltaTime="timeInterval"></MapCard>

      <b-button block :to="`/devices/${$route.params.id}/settings`">
        Edit Device<b-icon icon="pencil"> </b-icon>
      </b-button>
    </card>
  </div>
</template>

<script>
import StatsCard from "../components/Cards/StatsCard.vue";
import MapCard from "../components/Maps/MapCard.vue";
import * as Client from "../components/api/wheresMyThiefClient/index";

export default {
  name: "device-overview",
  components: {
    StatsCard,
    MapCard,
  },
  data() {
    return {
      mythief: {
        name: "",
        deviceTel: "",
        imei: "",
        image: "",
        status: "",
      },
      timeInterval: "0",
    };
  },
  methods: {
    /**
     *
     */
    setBatteryIndicator(value) {
      //get relevant HTMLElements and resets it's states
      var batteryElement = document.getElementById("battery-indicator");
      var batteryLabel = document.getElementById("battery-label");
      batteryElement.classList.remove("alert-level");
      batteryElement.classList.remove("warn-level");

      //make Number between [0.0,1.0]
      if (value > 1.0) value = 1.0;
      if (value < 0.0) value = 0.0;

      //Set indicatorlight
      if (value <= 0.5 && value > 0.2)
        batteryElement.classList.add("warn-level");
      if (value <= 0.2 && value >= 0.0)
        batteryElement.classList.add("alert-level");

      //Set Value
      batteryElement.style.height = `${100 * value}%`;
      batteryLabel.innerText = `${Math.floor(100 * value)}%`;
    },

    /**
     *
     */
    setQuoteOfTheUpdate() {
      var self = this;
      fetch("https://api.quotable.io/random")
        .then((response) => response.json())
        .then((data) => (self.mythief.qod = data.content));
    },

    /**
     *
     */
    getDeviceData() {
      var self = this;
      let apiInstance = new Client.DevicesApi();
      apiInstance.devicesImeiGet(this.$route.params.id).then((data) => {
        self.mythief.name = data.name;
        self.mythief.imei = data.imei;
        self.mythief.deviceTel = data.devicePhoneNumber;
        self.mythief.pin = localStorage.getItem(`devices/${data.imei}/pin`);
        self.mythief.image = localStorage.getItem(`devices/${data.imei}/image`);
        self.setBatteryIndicator(Math.floor(data.battery));
      });
    },
  },
  mounted: function () {
    this.getDeviceData();
  },
};
</script>

<style lang="scss">
$lightning-size: 18px;

.battery {
  border: 3px solid #333;
  width: 30px;
  height: 50px;
  padding: 2px;
  border-radius: 4px;
  position: relative;
  margin: 15px 0;

  &:before {
    content: "";
    height: 3px;
    width: 20px;
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

  &.warn-level {
    background-color: #efaf13;
  }

  &.alert-level {
    background-color: #e81309;

    &:before {
      background-image: url("data:image/svg+xml;charset=US-ASCII,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22utf-8%22%3F%3E%3C!DOCTYPE%20svg%20PUBLIC%20%22-%2F%2FW3C%2F%2FDTD%20SVG%201.1%2F%2FEN%22%20%22http%3A%2F%2Fwww.w3.org%2FGraphics%2FSVG%2F1.1%2FDTD%2Fsvg11.dtd%22%3E%3Csvg%20version%3D%221.1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20width%3D%2232%22%20height%3D%2232%22%20viewBox%3D%220%200%2032%2032%22%3E%3Cg%3E%3C%2Fg%3E%20%3Cpath%20fill%3D%22%23e81309%22%20d%3D%22M17.927%2012l2.68-10.28c0.040-0.126%200.060-0.261%200.060-0.4%200-0.726-0.587-1.32-1.314-1.32-0.413%200-0.78%200.187-1.019%200.487l-13.38%2017.353c-0.18%200.227-0.287%200.513-0.287%200.827%200%200.733%200.6%201.333%201.333%201.333h8.073l-2.68%2010.28c-0.041%200.127-0.060%200.261-0.060%200.4%200.001%200.727%200.587%201.32%201.314%201.32%200.413%200%200.78-0.186%201.020-0.487l13.379-17.353c0.181-0.227%200.287-0.513%200.287-0.827%200-0.733-0.6-1.333-1.333-1.333h-8.073z%22%3E%3C%2Fpath%3E%3C%2Fsvg%3E");
      background-repeat: no-repeat;
      background-size: $lightning-size;
      height: $lightning-size;
      width: $lightning-size;
      margin: -25px 0 0 -10px;
      content: "";
      display: inline-block;
      position: absolute;
    }
  }
}

.container {
  display: flex;
  justify-content: center;
  max-width: 800px;
}
</style>
