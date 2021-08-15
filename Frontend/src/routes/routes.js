import DashboardLayout from '../layout/DashboardLayout.vue'
import CenteredContentLayout from '../layout/CenteredContentLayout.vue'

//Where's my Thieve Pages
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import UserSettings from '../pages/UserSettings.vue'
import UserOverview from '../pages/UserOverview.vue'
import DeviceOverview from '../pages/DeviceOverview.vue'
import RegisterDevice from '../pages/RegisterDevice.vue'
import DeviceSettings from '../pages/DeviceSettings.vue'

const routes = [
  {
    path: '/',
    component: CenteredContentLayout,
    redirect: '/users/login',
    children: [
      {
        path: '/users/login',
        name: 'Login',
        component: Login,
      },
      {
        path: '/users/register',
        name: 'Register',
        component: Register,
      },
    ],
  },
  {
    path: '/users',
    component: DashboardLayout,
    children: [
      {
        path: '/users/:id',
        name: 'UserOverview',
        component: UserOverview,
      },
      {
        path: '/users/:id/settings',
        name: 'UserSettings',
        component: UserSettings,
      },
    ],
    beforeEnter: (to, from, next) => {
      sessionMiddleware(next);
    },
  },
  {
    path: '/devices',
    component: DashboardLayout,
    children: [
      {
        path: '/devices/register',
        name: 'RegisterDevice',
        component: RegisterDevice,
      },
      {
        path: '/devices/:id',
        name: 'DeviceOverview',
        component: DeviceOverview,
      },
      {
        path: '/devices/:id/settings',
        name: 'DeviceSettings',
        component: DeviceSettings,
      },
    ],
    beforeEnter: (to, from, next) => {
      sessionMiddleware(next);
    },
  },
  { path: '*', redirect: '/users/login' }
]

function sessionMiddleware(next) {
  var x = document.cookie.indexOf("session=") // Very poor
  if (x >= 0) {
    next();
  }
  else next({ name: 'Login' })
}

export default routes
