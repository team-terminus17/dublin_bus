<template >
  <div>
<v-autocomplete 
    v-model="route"
    :items="routes"
    @change="updateItems"
    @item-clicked="passRoute"
    :auto-select-one-item="false"
  >
  </v-autocomplete>
    <button  @click="selectDirection" id="direction">{{ this.direction_text }}</button>
  </div>
</template>

<script>
import 'v-autocomplete/dist/v-autocomplete.css'
export default {
name: "RouteSelection",
  data(){
  return{
    items:null,
    routes:null,
    route:null,
    direction:1,
    direction_text:'inbound'
  };
  },

  methods:{
  updateItems: function (value){
      this.routes=this.items.filter(item=>item.includes(value)).slice(0,5);
  },

  getRoutes:async function(){
      let url = '/routes';
      let response = await fetch(url);
      let data = await response.json();
      this.items=data.routes;
      this.routes=data.routes.slice(0,5);
  },

    passRoute: function (value){
    this.route = value;
    this.$emit("selectRoute",value, this.direction);
    },

    selectDirection: function () {
    if(this.direction === 1){
      //1 for inbound, 0 for outbound
      this.direction = 0;
      this.direction_text = "outbound";
    }
    else{
      this.direction = 1;
      this.direction_text = "inbound";
    }
    if(this.route != null){
      this.passRoute(this.route);
    }
    }
  },

  created() {
    this.getRoutes();
  }
}
</script>

<style>

</style>