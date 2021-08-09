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
  props:['routeinfo'],
  watch:{
    routeinfo(newval,oldval){
      this.getStops(newval);
    }
  },
  methods:{
    getStops:async function(routedir){
      let url = 'stops/'+ routedir[0]+ '/'+ routedir[1];
      let response = await fetch(url);
      let data = await response.json();
      this.items=data.stops;
      this.stops=data.stops;
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
      this.stops = this.items.filter(item=>item.stopName.includes(value)||item.stopNumber.toString().includes(value));
    },

    getLabel: function (stop){
      if(stop){
        return stop.stopName;
      }
      else return "";
    }
  },
}
</script>

<style scoped>

</style>