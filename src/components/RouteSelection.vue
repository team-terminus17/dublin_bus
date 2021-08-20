<template >
  <div>
    <v-autocomplete
      v-model="route"
      :items="routes"
      @change="updateItems"
      @item-clicked="passRoute"
      :auto-select-one-item="false"
      placeholder="Route"
    >
    </v-autocomplete>
    <button @click="selectDirection" id="direction" class="btn btn-warning">
      {{ this.direction_text }}
    </button>
  </div>
</template>

<script>
import "v-autocomplete/dist/v-autocomplete.css";
export default {
  name: "RouteSelection",
  data() {
    return {
      items: null,
      routes: null,
      route: null,
      direction: 1,
      direction_text: "inbound",
    };
  },
  methods: {
    updateItems: function (value) {
      this.routes = this.items
        .filter((item) => item.toLowerCase().includes(value.toLowerCase()));
    },

    getRoutes: async function () {
      let url = "/routes";
      let response = await fetch(url);
      let data = await response.json();
      this.items=data.routes;
      this.routes=data.routes;
  },
    passRoute: function (value) {
      this.route = value;
      this.$emit("selectRoute", value, this.direction);
    },

    selectDirection: function () {
      if (this.direction === 1) {
        //1 for inbound, 0 for outbound
        this.direction = 0;
        this.direction_text = "outbound";
      } else {
        this.direction = 1;
        this.direction_text = "inbound";
      }
      if (this.route != null) {
        this.passRoute(this.route);
      }
    },

    clearView: function (){
      this.route = null;
    }
  },

  created() {
    this.getRoutes();
  },
};
</script>

<style>
input{
  color: var(--font-color);
}

.v-autocomplete .v-autocomplete-input-group .v-autocomplete-input {
  position: relative;
  font-size: 1em;
  padding: 5px 15px;
  box-shadow: none;
  border: 1px solid var(--border-color);
  width: 100%;
  outline: none;
  background-color: var(--background-color);
  border-radius: var(--border-radius);
}

.v-autocomplete .v-autocomplete-list {
  z-index: 1000;
  width: 100%;
  height: 200px;
  overflow-y: auto;
  overflow-x: hidden;
  text-align: left;
  border: none;
  border-top: none;
  max-height: 400px;
  overflow-y: auto;
  /* border-bottom: 1px solid var(--border-color); */
  border-radius: var(--border-radius);
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item {
  cursor: pointer;
  color: var(--font-color);
  background-color: var(--background-color);
  padding: 10px;
  border-bottom: 1px solid var(--border-color);
  border-left: 1px solid var(--border-color);
  border-right: 1px solid var(--border-color);
  text-align: center;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item:hover {
  background-color: var(--border-color);
}

.v-autocomplete
  .v-autocomplete-list
  .v-autocomplete-list-item.v-autocomplete-item-active {
  background-color: var(--border-color);
}

#direction {
  margin-top: 1em;
}
</style>