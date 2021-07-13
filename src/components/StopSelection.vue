<template>
<!-- <div class="col-sm-12 col-md-2"  style="margin-top: 24px;"> -->
  <div class="col-sm-12 col-md-2">
<!-- <label class="d-flex justify-content-start">Origin Stop</label> -->
<v-autocomplete
    v-model="stop"
    :items="stops"
    @change="updateStops"
    @input="passStop"
    :component-item='template'
    :get-label='getLabel'
    :auto-select-one-item="false">
</v-autocomplete>
</div>
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
    getStops:async function(val){
      let url = 'stops/'+ val;
      let response = await fetch(url);
      let data = await response.json();
      this.items=Object.values(data.stops);
      this.stops=Object.values(data.stops);
  },
    passStop: function (value){
      if(value){
        this.$emit("stopSelected",value.id);
      }
      else{
        this.$emit("stopSelected",null);
      }
    },
    updateStops: function (value){
      this.stops = this.items.filter(item=>item.id.includes(value)||item.name.includes(value))
    },
    getLabel: function (stop){
      if(stop){
        return stop.name;
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