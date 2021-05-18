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
      <button
        class="btn btn-danger btn-fill float-right"
        v-b-modal.modal-call-police-guide
      >
        Call Police
      </button>

      <slot name="header">
        <h4 class="card-title">{{ title }}</h4>
      </slot>
      <p class="card-category" v-if="subTitle">{{ subTitle }}</p>
    </div>
    <div class="card-body">
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
    </div>
    <b-modal id="modal-call-police-guide" title="BootstrapVue" @ok="callPolice">
      <p class="my-4">Hello from modal!</p>
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

      //Push to all marker positons object
      this.markers.positions.push(newMarker);
      this.markers.points.push(newMarker.position);
      this.center = latLng(newMarker.position.lat, newMarker.position.lng);
      this.$nextTick(() => {
        this.$refs.marker[this.$refs.marker.length - 1].mapObject.openPopup();
      });
    },
  },
  mounted: function () {
    const self = this;
    window.setInterval(function () {
      self.addMarker(0.001 * Math.random() + 45.0, 0.001 * Math.random());
    }, 3000);
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
