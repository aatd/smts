/*!

 =========================================================
 * Vue Light Bootstrap Dashboard - v2.0.0 (Bootstrap 4)
 =========================================================

 * Product Page: http://www.creative-tim.com/product/light-bootstrap-dashboard
 * Copyright 2019 Creative Tim (http://www.creative-tim.com)
 * Licensed under MIT (https://github.com/creativetimofficial/light-bootstrap-dashboard/blob/master/LICENSE.md)

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 */

// Install Vue plugin
import Vue from 'vue'
import App from './App.vue'

// Install LightBootstrap plugin
import LightBootstrap from './light-bootstrap-main'
Vue.use(LightBootstrap)

// Install Vue-Router
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

// Install Serive Worker
import './registerServiceWorker'


// Install Leaflet Maps
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

// Import Bootstrap (order!)
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.prototype.$IsDebug = false;

// MAIN-Entrypoint!
new Vue({
  el: '#app',
  render: h => h(App),
  router
})
