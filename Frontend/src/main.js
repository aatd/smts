/*!

 =========================================================
 * Where's My Thief - Frontend-Application - v0.0.1
 =========================================================

 * Licensed under MIT (https://github.com/aatd/smts)

 =========================================================

 */

//#region Install Main Vue plugin
import Vue from 'vue'
import App from './App.vue'
//#endregion

//#region Install LightBootstrap plugin
import LightBootstrap from './light-bootstrap-main'
Vue.use(LightBootstrap)
//#endregion

//#region Install Vue-Router
import VueRouter from 'vue-router'
import routes from './routes/routes'
Vue.use(VueRouter)
const router = new VueRouter({
  routes: routes,
  linkActiveClass: 'nav-item active',
  scrollBehavior: (to) => {
    if (to.hash) {
      return { selector: to.hash }
    } else {
      return { x: 0, y: 0 }
    }
  }
})
//#endregion

//#region Install Serive Worker
import './registerServiceWorker'
//#endregion

//#region Install Leaflet Maps
import { LMap, LTileLayer, LMarker, LTooltip, LPopup } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';
import { Icon } from 'leaflet';
Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
Vue.component('l-tooltip', LTooltip);
Vue.component('l-popup', LPopup);
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});
//#endregion

//#region Import Bootstrap
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
//#endregion

// MAIN-Entrypoint!
Vue.prototype.$IsDebug = false;

new Vue({
  el: '#app',
  render: h => h(App),
  router
})
