import DashboardLayout from '../layout/DashboardLayout.vue'
import Content from 'src/layout/Content.vue'

// GeneralViews
import NotFound from '../pages/NotFoundPage.vue'

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
import UserOverview from 'src/components/Forms/UserOverview.vue'
import Device from 'src/components/Forms/Device.vue'

const routes = [

  //Entry is LoginPage
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/users'
  },
  {
    path: '/',
    component: Content,
    children: [
      {
        path: '/users',
        name: 'LoginPage',
        component: Login,
      },
      {
        path: '/users/:id',
        name: 'User-Overview',
        component: UserOverview,
      },
      {
        path: '/devices/:id',
        name: 'Device-Overview',
        component: Device
      }
    ]
  },
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

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes
