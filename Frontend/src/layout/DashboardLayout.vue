<template>
  <div class="wrapper">
    <top-navbar></top-navbar>
    <transition name="fade" mode="out-in">
      <router-view></router-view>
    </transition>
  </div>
</template>


<style lang="scss">
</style>

<script>
import TopNavbar from "./TopNavbar.vue";
export default {
  components: {
    TopNavbar,
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
  },
};
</script>
