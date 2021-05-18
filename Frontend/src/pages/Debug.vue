<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          <Device></Device>
        </div>
      </div>

      <!--User Profile Card-->
      <div class="row">
        <div class="col-md-12">
          <user-overview></user-overview>
        </div>
      </div>

      <!--User Profile Card-->
      <div class="row">
        <div class="col-md-12">
          <user-profile></user-profile>
        </div>
      </div>

      <!--Login Card-->
      <div class="row">
        <div class="col-md-12">
          <Login>
            <template slot="header">
              <h4 class="card-title">Login</h4>
              <p class="card-category">Login to your Bikes</p>
            </template>
            <template slot="footer">
              <div class="legend"></div>
              <hr />
              <div class="stats"></div>
            </template>
          </Login>
        </div>
      </div>

      <!--Register Card-->
      <div class="row">
        <div class="col-md-12">
          <Register>
            <template slot="header">
              <h4 class="card-title">
                Register your Account for "Where's my Thief?"
              </h4>
              <p class="card-category">
                Some information about you so you can set up your Bikes in the
                next step!
              </p>
            </template>
            <template slot="footer">
              <div class="legend"></div>
              <hr />
              <div class="stats"></div>
            </template>
          </Register>
        </div>
      </div>

      <!--Register Device Card-->
      <div class="row">
        <div class="col-md-12">
          <RegisterDevice>
            <template slot="header">
              <h4 class="card-title">Register new "My Thief" - Device</h4>
              <p class="card-category">
                This Form will create a inital Config-File to setup your
                "My-Thief"-Device
              </p>
            </template>
            <template slot="footer">
              <div class="legend"></div>
              <hr />
              <div class="stats"></div>
            </template>
          </RegisterDevice>
        </div>
      </div>

      <!--Device Settings Card-->
      <div class="row">
        <div class="col-md-12">
          <DeviceSettings>
            <template slot="header">
              <h4 class="card-title">Your Settings</h4>
              <p class="card-category">
                Here you see all your Settings and devices!
              </p>
            </template>
            <template slot="footer">
              <div class="legend"></div>
              <hr />
              <div class="stats"></div>
            </template>
          </DeviceSettings>
        </div>
      </div>

      <!--Simple Map-->
      <div class="row">
        <div class="col-md-12">
          <MapCard>
            <template slot="header">
              <h4 class="card-title">Bike Live Tracker</h4>
              <p class="card-category"></p>
            </template>
            <template slot="footer">
              <div class="legend">
                <i class="fa fa-circle text-info"></i> Tesla Model S
                <i class="fa fa-circle text-danger"></i> BMW 5 Series
              </div>
              <hr />
              <div class="stats">
                <i class="fa fa-check"></i> Data information certified
              </div>
            </template>
          </MapCard>
        </div>
      </div>

      <!--Generic Map with lots of Functions! -->
      <div class="row" v-if="isDebugMode">
        <div class="col-md-12">
          <map-card-test>
            <template slot="header">
              <h4 class="card-title">Test Map Card with multiple Options</h4>
            </template>
            <template slot="footer">
              <div class="legend"></div>
              <hr />
              <div class="stats"></div>
            </template>
          </map-card-test>
        </div>
      </div>

      <!--Some Stats Cards-->
      <div class="row">
        <div class="col-xl-4 col-md-6">
          <stats-card>
            <div slot="header" class="icon-warning">
              <i class="fa fa-bicycle text-warning"></i>
            </div>
            <div slot="content">
              <p class="card-category">Your Thief's</p>
              <h4 class="card-title">GETCOUNTOFMYTHIEFS</h4>
            </div>
            <div slot="footer"><i class="fa fa-plus"></i>Add new "Thief"</div>
          </stats-card>
        </div>

        <div class="col-xl-4 col-md-6">
          <stats-card>
            <div slot="header" class="icon-warning">
              <i class="fa fa-cogs text-warning"></i>
            </div>
            <div slot="content">
              <p class="card-category">Setup your Thief</p>
              <h4 class="card-title">GETCOUNTOFMYTHIEFS</h4>
            </div>
            <div slot="footer"><i class="fa fa-cogs"></i>Add new "Thief"</div>
          </stats-card>
        </div>

        <div class="col-xl-4 col-md-6">
          <stats-card>
            <div slot="header" class="icon-success">
              <i class="nc-icon nc-light-3 text-success"></i>
            </div>
            <div slot="content">
              <p class="card-category">Revenue</p>
              <h4 class="card-title">$1,345</h4>
            </div>
            <div slot="footer"><i class="fa fa-calendar-o"></i>Last day</div>
          </stats-card>
        </div>

        <div class="col-xl-4 col-md-6">
          <stats-card>
            <div slot="header" class="icon-danger">
              <i class="nc-icon nc-vector text-danger"></i>
            </div>
            <div slot="content">
              <p class="card-category">Errors</p>
              <h4 class="card-title">23</h4>
            </div>
            <div slot="footer"><i class="fa fa-clock-o"></i>Last day</div>
          </stats-card>
        </div>

        <div class="col-xl-4 col-md-6">
          <stats-card>
            <div slot="header" class="icon-info">
              <i class="nc-icon nc-favourite-28 text-primary"></i>
            </div>
            <div slot="content">
              <p class="card-category">Followers</p>
              <h4 class="card-title">+45</h4>
            </div>
            <div slot="footer"><i class="fa fa-refresh"></i>Updated now</div>
          </stats-card>
        </div>
      </div>

      <!--Some Line-Pie-Charts-->
      <div class="row">
        <div class="col-md-6">
          <chart-card
            :chart-data="lineChart.data"
            :chart-options="lineChart.options"
            :responsive-options="lineChart.responsiveOptions"
          >
            <template slot="header">
              <h4 class="card-title">Users Behavior</h4>
              <p class="card-category">24 Hours performance</p>
            </template>
            <template slot="footer">
              <div class="legend">
                <i class="fa fa-circle text-info"></i> Open
                <i class="fa fa-circle text-danger"></i> Click
                <i class="fa fa-circle text-warning"></i> Click Second Time
              </div>
              <hr />
              <div class="stats">
                <i class="fa fa-history"></i> Updated 3 minutes ago
              </div>
            </template>
          </chart-card>
        </div>
        <div class="col-md-6">
          <chart-card :chart-data="pieChart.data" chart-type="Pie">
            <template slot="header">
              <h4 class="card-title">Email Statistics</h4>
              <p class="card-category">Last Campaign Performance</p>
            </template>
            <template slot="footer">
              <div class="legend">
                <i class="fa fa-circle text-info"></i> Open
                <i class="fa fa-circle text-danger"></i> Bounce
                <i class="fa fa-circle text-warning"></i> Unsubscribe
              </div>
              <hr />
              <div class="stats">
                <i class="fa fa-clock-o"></i> Campaign sent 2 days ago
              </div>
            </template>
          </chart-card>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <chart-card
            :chart-data="barChart.data"
            :chart-options="barChart.options"
            :chart-responsive-options="barChart.responsiveOptions"
            chart-type="Bar"
          >
            <template slot="header">
              <h4 class="card-title">2014 Sales</h4>
              <p class="card-category">All products including Taxes</p>
            </template>
            <template slot="footer">
              <div class="legend">
                <i class="fa fa-circle text-info"></i> Tesla Model S
                <i class="fa fa-circle text-danger"></i> BMW 5 Series
              </div>
              <hr />
              <div class="stats">
                <i class="fa fa-check"></i> Data information certified
              </div>
            </template>
          </chart-card>
        </div>
      </div>

      <!--Tasksheets-->
      <div class="row">
        <div class="col-md-6">
          <card>
            <template slot="header">
              <h5 class="title">Tasks</h5>
              <p class="category">Backend development</p>
            </template>
            <l-table :data="tableData.data" :columns="tableData.columns">
              <template slot="columns"></template>

              <template slot-scope="{ row }">
                <td>
                  <base-checkbox v-model="row.checked"></base-checkbox>
                </td>
                <td>{{ row.title }}</td>
                <td class="td-actions text-right">
                  <button
                    type="button"
                    class="btn-simple btn btn-xs btn-info"
                    v-tooltip.top-center="editTooltip"
                  >
                    <i class="fa fa-edit"></i>
                  </button>
                  <button
                    type="button"
                    class="btn-simple btn btn-xs btn-danger"
                    v-tooltip.top-center="deleteTooltip"
                  >
                    <i class="fa fa-times"></i>
                  </button>
                </td>
              </template>
            </l-table>
            <div class="footer">
              <hr />
              <div class="stats">
                <i class="fa fa-history"></i> Updated 3 minutes ago
              </div>
            </div>
          </card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ChartCard from "src/components/Cards/ChartCard.vue";
import StatsCard from "src/components/Cards/StatsCard.vue";
import LTable from "src/components/Table.vue";
import MapCard from "src/components/Maps/MapCard.vue";
import MapCardTest from "src/components/Maps/MapCardTest.vue";
import Login from "src/components/Forms/Login.vue";
import Register from "src/components/Forms/Register.vue";
import RegisterDevice from "src/components/Forms/RegisterDevice.vue";
import DeviceSettings from "src/components/Forms/DeviceSettings.vue";
import UserProfile from "src/components/Forms/UserProfile.vue";
import UserOverview from "src/components/Forms/UserOverview.vue";
import Device from "src/components/Forms/Device.vue";

export default {
  components: {
    LTable,
    ChartCard,
    StatsCard,
    MapCard,
    MapCardTest,
    Login,
    Register,
    RegisterDevice,
    DeviceSettings,
    UserProfile,
    UserOverview,
    Device,
  },
  data() {
    return {
      editTooltip: "Edit Task",
      deleteTooltip: "Remove",
      pieChart: {
        data: {
          labels: ["40%", "20%", "40%"],
          series: [40, 20, 40],
        },
      },
      lineChart: {
        data: {
          labels: [
            "9:00AM",
            "12:00AM",
            "3:00PM",
            "6:00PM",
            "9:00PM",
            "12:00PM",
            "3:00AM",
            "6:00AM",
          ],
          series: [
            [287, 385, 490, 492, 554, 586, 698, 295],
            [67, 152, 143, 240, 287, 335, 435, 437],
            [23, 113, 67, 108, 190, 239, 307, 308],
          ],
        },
        options: {
          low: 0,
          high: 800,
          showArea: false,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: true,
          showLine: true,
          showPoint: true,
          fullWidth: true,
          chartPadding: {
            right: 50,
          },
        },
        responsiveOptions: [
          [
            "screen and (max-width: 640px)",
            {
              axisX: {
                labelInterpolationFnc(value) {
                  return value[0];
                },
              },
            },
          ],
        ],
      },
      barChart: {
        data: {
          labels: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "Mai",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
          ],
          series: [
            [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
            [412, 243, 280, 580, 453, 353, 300, 364, 368, 410, 636, 695],
          ],
        },
        options: {
          seriesBarDistance: 10,
          axisX: {
            showGrid: false,
          },
          height: "245px",
        },
        responsiveOptions: [
          [
            "screen and (max-width: 640px)",
            {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc(value) {
                  return value[0];
                },
              },
            },
          ],
        ],
      },
      tableData: {
        data: [
          {
            title:
              'Sign contract for "What are conference organizers afraid of?"',
            checked: false,
          },
          {
            title:
              "Lines From Great Russian Literature? Or E-mails From My Boss?",
            checked: true,
          },
          {
            title:
              "Flooded: One year later, assessing what was lost and what was found when a ravaging rain swept through metro Detroit",
            checked: true,
          },
          {
            title: "Create 4 Invisible User Experiences you Never Knew About",
            checked: false,
          },
          { title: 'Read "Following makes Medium better"', checked: false },
          { title: "Unfollow 5 enemies from twitter", checked: false },
        ],
      },
      user: {
        username: "Asef",
        email: "max.mustermann@max.de",
        firstName: "Max",
        lastName: "Mustermann",
      },
      isDebugMode: false,
    };
  },
  methods: {
    isDebugModeMethod() {
      const x = webpackHotUpdate;
      return x;
    },
  },
};
</script>

<style>
</style>
