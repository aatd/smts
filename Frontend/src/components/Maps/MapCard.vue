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
          @click="setAdress(marker)"
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
import * as Client from "../api/wheresMyThiefClient/index";

export default {
  name: "map-component",
  components: {
    LMap,
    LTileLayer,
    LControl,
    LPolyline,
    LLayerGroup,
  },
  props: {
    deltaTime: {
      type: String,
      required: false,
      //default: "100"
    },
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
    setAdress(marker) {
      console.log(marker);

      var self = this;

      var lat = marker.position.lat;
      var lng = marker.position.lng;

      fetch(
        `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`
      )
        .then((res) => res.json())
        .then((obj) => {
          marker.tooltip = `
            <b>Road: </b>${obj.address.road} ${
            obj.address.house_number || ""
          }<br />
            <b>City: </b>${obj.address.city || ""}  <br />
            <b>State: </b>${obj.address.state} <br />
            <b>Postal: </b>${obj.address.postcode}`;
          self.center = latLng(
            marker.position.lat,
            marker.position.lng - 0.001
          );
        });
    },
    /**
     * Adds a Marker to the and fills the map-component.
     * After adding it to it this method looks up the
     * adress based on the params given with
     * https://nominatim.org/release-docs/develop/
     *
     * @param {Number} latitude
     * @param {Number} longitude
     * @param {boolean} fetchAdress
     */
    addMarker: function (latitude, longitude, fetchAdress) {
      //Create new Marker object
      const newMarker = {
        position: { lat: latitude, lng: longitude },
        draggable: false,
        visible: true,
        tooltip: null,
      };

      var self = this;

      if (fetchAdress) {
        fetch(
          `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latitude}&lon=${longitude}`
        )
          .then((res) => res.json())
          .then((obj) => {
            newMarker.tooltip = `
            <b>Road: </b>${obj.address.road} ${
              obj.address.house_number || ""
            }<br />
            <b>City: </b>${obj.address.city} <br />
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
      } else {
        newMarker.tooltip = `
            <b>Lat: </b>${newMarker.position.lat}<br />
            <b>Lng: </b>${newMarker.position.lng} <br />`;
        self.markers.positions.push(newMarker);
        self.markers.points.push(newMarker.position);
        self.center = latLng(
          newMarker.position.lat,
          newMarker.position.lng - 0.001
        );
      }
    },
    receiveDevicePositions() {
      var self = this;

      if (self.$IsDebug) {
        self.addMarker(
          50.93393 + 0.001 * Math.random(),
          6.988509 + 0.001 * Math.random()
        );
      } else {
        var apiInstance = new Client.DevicesApi();
        var opts = undefined;

        if (this.deltaTime !== "0") {
          var startTime = new Date();
          startTime.setMinutes(startTime.getMinutes() - self.deltaTime);
          startTime.setHours(startTime.getHours());
          startTime = startTime.getTime();

          var endTime = new Date();
          endTime.setHours(endTime.getHours());
          endTime = endTime.getTime();

          opts = {
            start: startTime,
            end: endTime,
          };
        }

        apiInstance
          .devicesImeiLocationsGet(self.$route.params.id, opts)
          .then((data) => {
            // Check if locations are empty
            if (data == null || data == undefined) {
              console.log("No new Locations found!");
              return;
            }

            for (let i = 0; i < data.length; i++) {
              const currente_location = data[i];
              const isLastLocation = i === data.length - 1;
              let location = new Client.GPSPosition();
              location.longitude = currente_location.longitude;
              location.latitude = currente_location.latitude;

              self.addMarker(
                currente_location.latitude,
                currente_location.longitude,
                isLastLocation
              );
            }
          })
          .catch((error) => {
            console.log("Retrieving locations failed.");
          });
      }
    },
  },
  mounted: function () {
    this.receiveDevicePositions();
    this.addMarkerCallback = window.setInterval(
      this.receiveDevicePositions,
      this.$IsDebug ? 1000 : 5000
    );
  },
  beforeDestroy() {
    clearInterval(this.addMarkerCallback);
  },
  watch: {
    deltaTime: function (newVal, oldVal) {
      clearInterval(this.addMarkerCallback);
      this.receiveDevicePositions();

      if (newVal === "0") {
        this.addMarkerCallback = setInterval(
          this.receiveDevicePositions,
          this.$IsDebug ? 1000 : 5000
        );
      }

      if (newVal === "-1") {
        this.markers.positions = [];
        this.markers.points = [];
      }
    },
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
