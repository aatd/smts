<template>
  <div class="wrapper">
    <transition name="fade" mode="out-in">
      <div class="centered"><router-view></router-view></div>
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
export default {};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.centered {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 10vh;
}
</style>
