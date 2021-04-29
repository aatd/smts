<template>
  <div class="card" :class="[type && `card-${type}`]">
    <div class="card-image" v-if="$slots.image">
      <slot name="image"></slot>
    </div>
    <div
      class="card-header"
      v-if="$slots.header || title"
      :class="headerClasses"
    >
      <slot name="header">
        <h4 class="card-title">{{ title }}</h4>
        <p class="card-category" v-if="subTitle">{{ subTitle }}</p>
      </slot>
    </div>
    <div class="card-body">
      <l-map :zoom="zoom" :center="center" style="height: 400px">
        <l-marker
          v-for="marker in markers"
          :key="marker.id"
          :visible="marker.visible"
          :draggable="marker.draggable"
          :lat-lng.sync="marker.position"
          :icon="marker.icon"
          @click="alert(marker)"
        >
          <l-popup :content="marker.tooltip" />
          <l-tooltip :content="marker.tooltip" />
        </l-marker>

        <l-tile-layer :url="url" :attribution="attribution" />
      </l-map>
    </div>
    <slot name="raw-content"></slot>
    <div class="card-footer" :class="footerClasses" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LControl } from "vue2-leaflet";

export default {
  name: "map-card",
  components: {
    LMap,
    LTileLayer,
    LControl,
  },
  data() {
    return {
      zoom: 13,
      center: latLng(47.41322, -1.219482),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      markers: [
        {
          id: "m1",
          position: { lat: 51.505, lng: -0.09 },
          tooltip: "tooltip for marker1",
          draggable: true,
          visible: true,
        },
        {
          id: "m2",
          position: { lat: 51.8905, lng: -0.09 },
          tooltip: "tooltip for marker2",
          draggable: true,
          visible: false,
        },
        {
          id: "m3",
          position: { lat: 51.005, lng: -0.09 },
          tooltip: "tooltip for marker3",
          draggable: true,
          visible: true,
        },
      ],
    };
  },
  methods: {
    alert(item) {
      alert("this is " + JSON.stringify(item));
    },
    addMarker: function (latitude, longitude) {
      const newMarker = {
        position: { lat: latitude, lng: longitude },
        draggable: true,
        visible: true,
      };
      this.markers.push(newMarker);
      this.center = latLng(newMarker.position.lat, newMarker.position.lng)
    },
    removeMarker: function (index) {
      this.markers.splice(index, 1);
    },
    fitPolyline: function () {
      const bounds = latLngBounds(markers1.map((o) => o.position));
      this.bounds = bounds;
    }
  },
  mounted: function(){
    const self = this;
       window.setInterval(function(){
        const newMarker = {
          position: { lat: Math.random(), lng: Math.random() },
          draggable: true,
          visible: true,
        };
      self.markers.push(newMarker);
      self.center = latLng(newMarker.position.lat, newMarker.position.lng)
    }, 2000);
  },
  props: {
    title: {
      type: String,
      description: "Card title",
    },
    subTitle: {
      type: String,
      description: "Card subtitle",
    },
    type: {
      type: String,
      description: "Card type (e.g primary/danger etc)",
    },
    headerClasses: {
      type: [String, Object, Array],
      description: "Card header css classes",
    },
    bodyClasses: {
      type: [String, Object, Array],
      description: "Card body css classes",
    },
    footerClasses: {
      type: [String, Object, Array],
      description: "Card footer css classes",
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