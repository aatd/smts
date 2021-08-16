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
          ref="marker"
        >
          <l-popup ref="popup" :content="marker.tooltip" />
          <l-tooltip :content="marker.tooltip" />
        </l-marker>
        <l-polyline :lat-lngs="markers.points" />
      </l-layer-group>
      <l-tile-layer :url="url" :attribution="attribution" />
    </l-map>
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
import * as Client from "../api/wheresMyThiefClient/index";

export default {
  name: "map-component",
  components: {
    LMap,
    LTileLayer,
    LControl,
    BModal,
    LPolyline,
    LLayerGroup,
  },
  props: {
    deltaTime: String,
  },
  data() {
    return {
      zoom: 17,
      center: latLng(50.93393, 6.988509),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      markers: {
        positions: [],
        points: [],
      },
    };
  },
  methods: {
    /**
     * Adds a Marker to the and fills the map-component.
     * After adding it to it this method looks up the
     * adress based on the params given with
     * https://nominatim.org/release-docs/develop/
     *
     * @param {Number} latitude
     * @param {Number} longitude
     */
    addMarker: function (latitude, longitude) {
      //Create new Marker object
      const newMarker = {
        position: { lat: latitude, lng: longitude },
        draggable: false,
        visible: true,
        tooltip: "",
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
    var self = this;

    var updateTime = this.$IsDebug ? 5000 : 20000;

    self.addMarkerCallback = window.setInterval(function () {
      if (self.$IsDebug) {
        self.addMarker(
          50.93393 + 0.001 * Math.random(),
          6.988509 + 0.001 * Math.random()
        );
      } else {
        var apiInstance = new Client.DevicesApi();

        apiInstance
          .devicesImeiLocationsGet(self.$route.params.id)
          .then((data) => {
            if (data == null) {
              console.log("No new Locations found!");
              return;
            }
            let location = new Client.GPSPosition();
            location.longitude = data.longitude;
            location.latitude = data.latitude;
            self.addMarker(location.latitude, location.longitude);
          })
          .catch((error) => {
            console.log("Retrieving locations failed.");
          });
      }
    }, updateTime);
  },
  beforeDestroy() {
    clearInterval(this.addMarkerCallback);
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
</style>
