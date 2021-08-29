<template>
  <div class="bgImage">
    <top-navbar></top-navbar>
    <transition name="fade" mode="out-in">
      <router-view class="where-is-my-thief-wrapper"></router-view>
    </transition>
    <div class="modals">
      <b-modal
        id="loading-modal"
        centered
        title="BootstrapVue"
        hide-footer
        hide-header
        size="sm"
      >
        <div class="d-flex justify-content-center mb-3">
          <b-spinner label="Loading..."></b-spinner>
          <p>Loading...</p>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
export default {
  components: {
    TopNavbar,
  },
};
</script>

<style lang="scss">
.bgImage {
  background: url(/img/bg.jpg) no-repeat center center fixed;
  min-height: 100vh;
}
.where-is-my-thief-container {
  max-width: 400px;
  margin: auto;
  margin-top: 20px;
}

.where-is-my-thief-container-avatar {
  max-width: 400px;
  margin: auto;
  margin-top: 120px;
}
.where-is-my-thief-wrapper {
  padding-bottom: 100px;
}
</style>
