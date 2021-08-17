<template>
  <div>
    <Timeline
      id="dublinbusnews"
      sourceType="profile"
      widget-class="twitter"
      :options="theme"
  />
  </div>
</template>

<script>
import {Timeline} from "vue-tweet-embed";

export default {
name: "Twitter",

  components:{
  Timeline
  },

  data(){
  return{
    theme:{theme:'light'}
  }
  },

  props:['mode'],

  watch:{
  mode(val){
    this.theme= {theme:val};
    this.$forceUpdate();
  }
  }
}
</script>

<style scoped>
.twitter {
  max-height: 450px;
  overflow-y: auto;
}
</style>