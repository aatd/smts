<template>
  <div class="bgImage">
    <top-navbar></top-navbar>
    <transition name="fade" mode="out-in">
      <router-view></router-view>
    </transition>
  </div>
</template>


<style lang="scss">
.bgImage {
  background: url(/img/bg.jpg) no-repeat center center fixed;
  min-height: 100vh;
}
</style>

<script>
import TopNavbar from "./TopNavbar.vue";
export default {
  components: {
    TopNavbar,
  },
};
</script>
