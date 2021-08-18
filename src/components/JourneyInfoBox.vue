<template>
<div class="info-box">
  <div class="row">
    <div class="col-3" style="font-weight: bolder">
      <div class="row">
        <img :src="img_link"/>
      </div>
      <div class="row">
        <span>{{item.busroute}}</span>
      </div>
    </div>
    <div class="col-9">
      <div class="row">
        <div class="col-2"></div>
        <div class="col-10" style="text-align: center;font-weight: bolder">
          <span style="vertical-align:center;">{{item.time}}</span>
        </div>
      </div>
      <div class="row">
        <div v-html="item.instruction"></div>
      </div>
    </div>
  </div>
  <br v-if="item.mode=='bus'">
  <div style="padding-bottom: 10px">
     <Notification
          v-if="item.mode=='bus'&&item.trackable==true"
          :stop_dep="item.stop_dep"
          :stop_arr="item.stop_arr"
          :direction="item.direction"
          :route="item.route"
      ></Notification>
  </div>
</div>
</template>

<script>
import Notification from "@/components/Notification";
export default {
  name: "JourneyInfoBox",

  components:{
    Notification,
  },

  props:['item','mode'],

  watch:{
    mode(val){
      this.setImg();
    }
  },

  data(){
    return{
      img_link:null,
    }
  },

  methods:{
    setImg:function (){
      if(this.mode==='dark'){
        this.img_link = this.item.mode=='bus'?"https://img.icons8.com/material-rounded/48/ffffff/bus.png":
            "https://img.icons8.com/material-outlined/48/ffffff/walking--v1.png";
      }
      else{
        this.img_link = this.item.mode=='bus'?"https://img.icons8.com/fluency-systems-regular/48/000000/bus.png":
        "https://img.icons8.com/fluency-systems-filled/48/000000/walking.png";
      }
    }
  },

  created() {
    this.setImg();
  }
}
</script>

<style scoped>
.info-box{
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
  margin: 20px;
}
</style>