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
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}
</style>
