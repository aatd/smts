<template>
  <div class="centered" name="fade" mode="out-in">
    <router-view></router-view>
  </div>
</template>

<script>
export default {};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s;
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
