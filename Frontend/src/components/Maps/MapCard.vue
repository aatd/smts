<template>
  <card class="card-user register-container">
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
  </card>
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
            <b>Road: </b>${obj.address.road} <br />
            <b>County: </b>${obj.address.county} <br /> 
            <b>Municipality: </b>${obj.address.municipality} <br /> 
            <b>Postal: </b>${obj.address.postcode} <br /> 
            <b>Country: </b>${obj.address.country_code}`;
          self.markers.positions.push(newMarker);
          self.markers.points.push(newMarker.position);
          self.center = latLng(newMarker.position.lat, newMarker.position.lng);

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
    self.addRandomMarker = window.setInterval(function () {
      self.addMarker(0.001 * Math.random() + 45.0, 0.01 * Math.random());
    }, 4000);
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
