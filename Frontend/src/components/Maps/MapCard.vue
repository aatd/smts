<template>
  <div>
    <l-map :zoom="zoom" :center="center" style="height: 300px">
      <l-layer-group>
        <l-marker
          v-for="marker in markers.positions"
          :key="marker.id"
          :visible="marker.visible"
          :draggable="marker.draggable"
          :lat-lng.sync="marker.position"
          :icon="marker.icon"
          @click="alert(marker)"
          ref="marker"
        >
          <l-popup ref="popup" :content="marker.tooltip" />
          <l-tooltip :content="marker.tooltip" />
        </l-marker>
        <l-polyline :lat-lngs="markers.points" />
      </l-layer-group>
      <l-tile-layer :url="url" :attribution="attribution" />
    </l-map>
    <b-modal
      id="callPoliceModal"
      title="Call your local Authoroties!"
      @ok="callPolice"
    >
      <p>Some adivce when Calling them for real!</p>
      <ul class="list-group">
        <li class="list-group-item">Stay Calm!</li>
      </ul>
    </b-modal>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import {
  LMap,
  LTileLayer,
  LControl,
  LPolyline,
  LLayerGroup,
} from "vue2-leaflet";
import { BModal } from "bootstrap-vue";
import * as Client from "src/components/api/index";

export default {
  name: "map-card",
  components: {
    LMap,
    LTileLayer,
    LControl,
    BModal,
    LPolyline,
    LLayerGroup,
  },
  data() {
    return {
      zoom: 17,
      center: latLng(47.41322, -1.219482),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      markers: {
        positions: [],
        points: [],
      },
      client: new Client.DevicesApi(),
    };
  },
  methods: {
    callPolice: function () {
      window.location.href = "tel:110";
    },
    alert(item) {
      alert("this is " + JSON.stringify(item));
    },
    addMarker: function (latitude, longitude) {
      //Create new Marker object
      const newMarker = {
        position: { lat: latitude, lng: longitude },
        draggable: false,
        visible: true,
        tooltip: "Hello",
      };

      var self = this;

      fetch(
        `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latitude}&lon=${longitude}`
      )
        .then((res) => res.json())
        .then((obj) => {
          console.log(obj);
          newMarker.tooltip = `
            <b>Road: </b>${obj.address.road} ${obj.address.house_number}<br />
            <b>City: </b>${obj.address.city_district} <br />
            <b>State: </b>${obj.address.state} <br />
            <b>Postal: </b>${obj.address.postcode}`;
          self.markers.positions.push(newMarker);
          self.markers.points.push(newMarker.position);
          self.center = latLng(
            newMarker.position.lat,
            newMarker.position.lng - 0.001
          );

          if (self.markers.positions.length > 1) {
            this.$nextTick(() => {
              //Current Marker
              this.$refs.marker[
                this.$refs.marker.length - 1
              ].mapObject.openTooltip();

              //Last Marker
              this.$refs.marker[
                this.$refs.marker.length - 2
              ].mapObject.closeTooltip();
            });
          }
        });
    },
  },
  mounted: function () {
    const self = this;

    fetch(`http://intern.bewegtbildhelden.de/devices/865067020621788/locations`)
      .then((res) => res.json())
      .then((loc) => {
        self.addMarker(loc.latitude, loc.longitude);
      });

    self.addRandomMarker = window.setInterval(function () {
      fetch(
        `http://intern.bewegtbildhelden.de/devices/865067020621788/locations`
      )
        .then((res) => res.json())
        .then((loc) => {
          self.addMarker(loc.latitude, loc.longitude);
        });
    }, 20000);
  },
  beforeDestroy() {
    clearInterval(this.addRandomMarker);
  },
};
</script>

<style>
.example-custom-control {
  background: #fff;
  padding: 0 0.5em;
  border: 1px solid #aaa;
  border-radius: 0.1em;
}
.custom-control-watermark {
  font-size: 200%;
  font-weight: bolder;
  color: #aaa;
  text-shadow: #555;
}
.container {
  display: flex;
  justify-content: center;
  max-width: 800px;
}
</style>
