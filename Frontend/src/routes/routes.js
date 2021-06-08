import DashboardLayout from '../layout/DashboardLayout.vue'
import CenteredContent from 'src/layout/CenteredContent.vue'

// GeneralViews
import NotFound from 'src/pages/NotFoundPage.vue'

// Admin pages
import Overview from 'src/pages/Overview.vue'
import UserProfile from 'src/pages/UserProfile.vue'
import TableList from 'src/pages/TableList.vue'
import Typography from 'src/pages/Typography.vue'
import Icons from 'src/pages/Icons.vue'
import Notifications from 'src/pages/Notifications.vue'
import Upgrade from 'src/pages/Upgrade.vue'


//Where's my Thieve Pages
import Debug from 'src/pages/Debug.vue'
import Login from 'src/components/Forms/Login.vue'
import Register from 'src/components/Forms/Register.vue'
import UserOverview from 'src/components/Forms/UserOverview.vue'
import DeviceOverview from 'src/components/Forms/DeviceOverview.vue'
import RegisterDevice from 'src/components/Forms/RegisterDevice.vue'
import DeviceSettings from 'src/components/Forms/DeviceSettings.vue'
import UserSettings from 'src/components/Forms/UserSettings.vue'

const routes2 = [

  {
    path: '/admin',
    component: DashboardLayout,
    redirect: '/admin/overview',
    children: [

      // Where's My Thief-Pages
      {
        path: 'debug',
        name: 'Debug',
        component: Debug
      },



      //Delete Later
      {
        path: 'overview',
        name: 'Overview',
        component: Overview
      },
      {
        path: 'user',
        name: 'User',
        component: UserProfile
      },
      {
        path: 'table-list',
        name: 'Table List',
        component: TableList
      },
      {
        path: 'typography',
        name: 'Typography',
        component: Typography
      },
      {
        path: 'icons',
        name: 'Icons',
        component: Icons
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: Notifications
      },
      {
        path: 'upgrade',
        name: 'Upgrade to PRO',
        component: Upgrade
      }
    ]
  },

  //My Thieve Devices
  {
    path: '/mythieves',
    component: DashboardLayout,
    children: [
      {
        path: ':id',
        name: 'DevicePage',
        component: UserProfile,
      },

    ]

  },

  { path: '*', component: NotFound }
]


const routes = [
  {
    path: '/',
    component: CenteredContent,
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
    ]
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
    ]
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

    ]
  },
  { path: '*', redirect: '/users/login' }
]

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes
