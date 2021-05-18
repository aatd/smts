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
    </div>
  </div>
</template>

<script>
import StatsCard from "src/components/Cards/StatsCard.vue";
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
