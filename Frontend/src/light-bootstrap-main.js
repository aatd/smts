import VTooltip from 'v-tooltip'
import Notifications from './components/NotificationPlugin'
import GlobalComponents from './globalComponents'
import GlobalDirectives from './globalDirectives'
import 'bootstrap/dist/css/bootstrap.css'
import './assets/sass/light-bootstrap-dashboard.scss'
import './assets/css/demo.css'

export default {
  install(Vue) {
    Vue.use(GlobalComponents)
    Vue.use(GlobalDirectives)
    Vue.use(Notifications)
    Vue.use(VTooltip)
  }
}
