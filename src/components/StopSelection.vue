<template>
<v-autocomplete
    v-model="stop"
    :items="stops"
    @change="updateStops"
    @item-clicked="passStop">
</v-autocomplete>
</template>

<script>
import 'v-autocomplete/dist/v-autocomplete.css'
import bus from "@/components/bus";
export default {
  name: "StopSelection",
  data(){
    return{
      stop:null,
      stops:null,
    };
  },
  methods:{
    getStops:async function(val){
      let url = 'stops/'+ val;
      let response = await fetch(url);
      let data = await response.json();
      console.log(data.stops)
      console.log(Object.values(data.stops));
      this.items=Object.values(data.stops);
      this.stops=Object.values(data.stops);
  },
    passStop: function (val){
      console.log(val)
    },
    updateStops: function (value){
      this.stops = this.items.filter(item=>item.includes(value))
    }
  },
  created() {
    bus.$on("showRoute",this.getStops)
  }
}
</script>

<style scoped>

</style>