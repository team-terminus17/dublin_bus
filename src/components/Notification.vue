<template>
<div>
  <button class="btn btn-warning"
      @click="startTracking"
      @dblclick="cancelTracking"
  >{{this.button_text}}</button>
  <span>{{this.time_text}}</span>
</div>
</template>

<script>
const NOT_TRACKING = 0;
const TRACKING_DEPARTURE =1;
const TRACKING_ARRIVAL =2;
export default {
  name: "notification",

  props:['stop_dep','stop_arr','direction','route'],

  data(){
    return{
      button_text : "Track departure stop",
      time_text : null,
      status : NOT_TRACKING,//0 for not tracking, 1 for tracking departure stop, 2 for tracking arrival stop
      timerID : null,
      lat: null,
      lon: null,
      depNotificationRecord:new Set(),
      // This is for recording whether a notification has been pushed for each trip
      // to avoid pushing the notification frequently for each trip
    }
  },

  methods:{
    startTracking: function (){
      if(this.status===NOT_TRACKING){
        //We only allow tracking one bus journey at a time
        if(this.$store.state.trackingStatus===true){
          alert("You are tracking another bus journey at the moment.\n" +
              "Please cancel that to enable the tracking of this journey");
        }

        else{
          this.status=TRACKING_DEPARTURE;
          this.button_text="Track end stop";
          this.$store.commit("changeTrackingStatus",true);
          this.timerID = window.setInterval(this.trackDepStop,30*1000);
          this.trackDepStop();
        }
      }
      //Start tracking the arrival stop
      else if(this.status===TRACKING_DEPARTURE){
        this.button_text="Already off";
        this.time_text="";
        this.status=TRACKING_ARRIVAL;
        window.clearInterval(this.timerID);
        this.timerID = window.setInterval(this.trackArrStop,30*1000);//Refresh every half minute
      }

      else {
        this.cancelTracking();
      }
    },

    trackArrStop: function (){
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(res =>{
          let user_lat = res.coords.latitude;
          let user_lon = res.coords.longitude;
          let distance = this.getDistance(this.lat, this.lon, user_lat, user_lon);
          //Push the notification to user if he/she is within 0.5 km of the destination
          if(distance<0.5){
            const title = 'Reminder';
            const options = {
            body: 'You are getting closer to your destination. Please be ready to get off.'
          };

            navigator.serviceWorker.ready.then(function (registration){
                registration.showNotification(title,options);
            });

            this.cancelTracking();
          }
        });
      }
      else {
          alert("Geolocation is not supported by this browser.");
          this.cancelTracking();
      }
    },

    trackDepStop: async function (){
      let data = await this.fetchArrivalInfo();
      if(!data.trackable){
        alert("Sorry, this trip is not trackable");
        this.cancelTracking();
        return;
      }

      let waitingTime = data.time;
      let tripID = data.trip;
      this.time_text = ' in '+waitingTime+' mins'
      //Avoid pushing notifications of one trip for multiple times
      if(this.depNotificationRecord.has(tripID)) return;

      if(waitingTime<=3){
        this.depNotificationRecord.add(tripID)
        const title = 'Reminder';
            const options = {
            body: 'Bus is coming in ' + waitingTime + ' minutes. Please be ready.'
          };

            navigator.serviceWorker.ready.then(function (registration){
                registration.showNotification(title,options);
            });
      }

    },

    cancelTracking: function (){
      if (this.timerID) window.clearInterval(this.timerID);
      this.time_text = ""
      this.depNotificationRecord = new Set();
      this.status=NOT_TRACKING;
      this.$store.commit("changeTrackingStatus",false);
      this.button_text="Track departure stop";
    },

    getDistance:function (lat1, lon1, lat2, lon2) {
      //link to the code source:
      //https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
      const p = 0.017453292519943295;    // Math.PI / 180
      const c = Math.cos;

      let a = 0.5 - c((lat2 - lat1) * p)/2 +
              c(lat1 * p) * c(lat2 * p) *
              (1 - c((lon2 - lon1) * p))/2;

      return 12742 * Math.asin(Math.sqrt(a));
    },

    fetchArrivalInfo: async function(){
      let timeUrl = `/time/${this.route}/${this.stop_dep}/${this.direction}`;
      let response = await fetch(timeUrl);
      let data = await response.json();
      return data;
    }
  },

  created() {
    fetch(`/stop/${this.stop_arr}/coordinates`)
      .then(response => response.json())
      .then(data => {
        this.lat=data[0].lat;
        this.lon=data[0].lon;
    });
  },

  beforeDestroy() {
    if (this.timerID) window.clearInterval(this.timerID);
    this.$store.commit("changeTrackingStatus",false);
  }
}
</script>

<style scoped>

</style>