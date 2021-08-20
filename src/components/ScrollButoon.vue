<template>
  <div id="scroll">
    <a href="#input-content">
      <img :src=img_link[mode]>
    </a>
  </div>
</template>

<script>
export default {
  name: "ScrollButoon",

  data(){
    return{
      img_link:{
        'light':'https://img.icons8.com/ios-filled/50/347aa0/down-squared--v2.png',
        'dark':'https://img.icons8.com/ios-filled/50/d59563/down-squared--v2.png'
      },
    }
  },

  props:['mode'],

  computed: {
    map() {
      return this.$store.state.map;
    },
  },

  watch:{
  map(){
    this.initAuto();
  }
  },

  methods: {
    initAuto: function () {
      const controlDiv = document.getElementById("scroll");
      this.map.controls[window.google.maps.ControlPosition.BOTTOM_CENTER].push(controlDiv);
    },
  }
}
</script>

<style scoped>
#scroll{
  visibility: hidden;
  margin: 20px 20px !important;
}
@media only screen and (max-width: 992px){
  #scroll{
    visibility: visible;
  }
}
</style>