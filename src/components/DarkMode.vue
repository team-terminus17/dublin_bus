<template>
  <button
      id="dark"
      class="btn btn-warning"
      style="margin: 50px 20px"
      @click="changeMode"
  >
    {{ mode }}
  </button>
</template>

<script>
export default {
  name: "DarkMode",

  data(){
    return{
      mode: 'Dark',
    }
  },

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

  methods:{
    initAuto: function (){
      const controlDiv = document.getElementById("dark");
      this.map.controls[window.google.maps.ControlPosition.TOP_RIGHT].push(controlDiv);
    },

    changeMode: function (){
      this.changeMap();
      this.$emit('changeMode', this.mode.toLowerCase());
      this.mode = this.mode === 'Dark'? 'Light':'Dark';
    },

    changeMap: function (){
      if(this.mode==='Dark'){
        this.map.setOptions({styles:[
      { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
      { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
      { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
      {
        featureType: "administrative.locality",
        elementType: "labels.text.fill",
        stylers: [{ color: "#d59563" }],
      },
      {
        featureType: "poi",
        elementType: "labels.text.fill",
        stylers: [{ color: "#d59563" }],
      },
      {
        featureType: "poi.park",
        elementType: "geometry",
        stylers: [{ color: "#263c3f" }],
      },
      {
        featureType: "poi.park",
        elementType: "labels.text.fill",
        stylers: [{ color: "#6b9a76" }],
      },
      {
        featureType: "road",
        elementType: "geometry",
        stylers: [{ color: "#38414e" }],
      },
      {
        featureType: "road",
        elementType: "geometry.stroke",
        stylers: [{ color: "#212a37" }],
      },
      {
        featureType: "road",
        elementType: "labels.text.fill",
        stylers: [{ color: "#9ca5b3" }],
      },
      {
        featureType: "road.highway",
        elementType: "geometry",
        stylers: [{ color: "#746855" }],
      },
      {
        featureType: "road.highway",
        elementType: "geometry.stroke",
        stylers: [{ color: "#1f2835" }],
      },
      {
        featureType: "road.highway",
        elementType: "labels.text.fill",
        stylers: [{ color: "#f3d19c" }],
      },
      {
        featureType: "transit",
        elementType: "geometry",
        stylers: [{ color: "#2f3948" }],
      },
      {
        featureType: "transit.station",
        elementType: "labels.text.fill",
        stylers: [{ color: "#d59563" }],
      },
      {
        featureType: "water",
        elementType: "geometry",
        stylers: [{ color: "#17263c" }],
      },
      {
        featureType: "water",
        elementType: "labels.text.fill",
        stylers: [{ color: "#515c6d" }],
      },
      {
        featureType: "water",
        elementType: "labels.text.stroke",
        stylers: [{ color: "#17263c" }],
      },
    ]})
      }
      else{
          this.map.setOptions({
            styles:[]
          })
      }
    }
  }
}
</script>

<style scoped>

</style>