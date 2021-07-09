<template>
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
    bus.$emit("showRoute",value)
    }
  },
  created() {
    this.getRoutes();
  }
}
</script>

<style scoped>

</style>