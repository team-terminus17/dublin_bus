<template>
<v-autocomplete
    v-model="stop"
    :items="stops"
    @change="updateStops"
    @input="passStop"
    :component-item='template'
    :get-label='getLabel'
    :auto-select-one-item="false">
</v-autocomplete>
</template>

<script>
import 'v-autocomplete/dist/v-autocomplete.css'
import bus from "@/components/bus";
import StopTemplate from "@/components/StopTemplate";
export default {
  name: "StopSelection",
  data(){
    return{
      stop:null,
      stops:null,
      items:null,
      template: StopTemplate
    };
  },
  methods:{
    getStops:async function(){
      let url = 'stops/'+ arguments[0]+ '/'+ arguments[1];
      let response = await fetch(url);
      let data = await response.json();
      this.items=data.stops;
      this.stops=data.stops.slice(0,5);
  },
    passStop: function (value){
      if(value){
        this.$emit("stopSelected",value.stopID);
      }
      else{
        this.$emit("stopSelected",null);
      }
    },
    updateStops: function (value){
      this.stops = this.items.filter(item=>item.stopName.includes(value)||item.stopNumber.toString().includes(value)).slice(0,5)
    },
    getLabel: function (stop){
      if(stop){
        return stop.stopName;
      }
      else return "";
    }
  },
  created() {
    bus.$on("showRoute",this.getStops)
  }
}
</script>

<style scoped>

</style>