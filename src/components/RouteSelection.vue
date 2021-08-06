<template >
<v-autocomplete 
    v-model="route"
    :items="routes"
    @change="updateItems"
    @item-clicked="passRoute"
  >
  </v-autocomplete>
</template>

<script>
import 'v-autocomplete/dist/v-autocomplete.css'
import bus from "@/components/bus";
export default {
name: "RouteSelection",
  data(){
  return{
    items:null,
    routes:null,
    route:null
  };
  },
  methods:{
  updateItems(value){
      this.routes=this.items.filter(item=>item.includes(value))
  },
  getRoutes:async function(){
      let url = '/routes';
      let response = await fetch(url);
      let data = await response.json();
      console.log(data.routes)
      this.items=data.routes;
      this.routes=data.routes;
  },
    passRoute(value){
    this.$emit("selectRoute",value)
    bus.$emit("showRoute",value)
    }
  },
  created() {
    this.getRoutes();
  }
}
</script>

<style>

.v-autocomplete .v-autocomplete-input-group .v-autocomplete-input {
  position: relative;
  font-size: 1.0em;
  padding: 5px 15px;
  box-shadow: none;
  border: 1px solid #157977;
  width: 100%;
  outline: none;
  background-color: 	#bbd7f2;
  border-radius: 8px;
  }

.v-autocomplete .v-autocomplete-list{
  z-index: 1000;
  width: 100%;
  height: 200px;
  overflow-y:auto;
  overflow-x: hidden;
  text-align: left;
  border: none;
  border-top: none;
  max-height: 400px;
  overflow-y: auto;
  border-bottom: 1px solid #157977;
  border-radius: 8px;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item{
  cursor: pointer;
  color: black;
  background-color: #bbdaa4;
  padding: 10px;
  border-bottom: 1px solid #157977;
  border-left: 1px solid #157977;
  border-right: 1px solid #157977;
  text-align: center;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item:hover{
  background-color: 	#bbd7f2;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item.v-autocomplete-item-active {
  background-color:	#bbd7f2;
}

</style>