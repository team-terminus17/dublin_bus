<template>
  <div>
    <b v-if="this.item.stopNumber>0">#{{item.stopNumber}}</b>
    <span>{{ item.stopName }}</span>
  </div>

</template>

<script>
export default {
  name: "StopTemplate",
  props: {
    item: { required: true },
  }
}
</script>

<style scoped>

</style>