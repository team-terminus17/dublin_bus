<template>
    <div>
    <div class="col-sm-12 col-md-4 d-flex justify-content-start card rounded my-3 shadow-lg back-card overflow-hidden">
        <div class="card-body">
        <div class="card-mid">
            <div class="row">
                <div class="col-md-4 text-center temp">
                <span>{{weather.temp}}&deg;C</span>
                <p class="my-4">Rain:{{weather.description}}</p>
                </div>
                <div class="col-md-4">
                <span>{{weather.icon}}</span>
                </div>
                <div class="col-md-4">
                <p>{{weather.cityName}}</p>
                <p class="">{{weather.country}}</p>
                </div>
            </div>
        </div>
        </div>
    </div>
    </div>
</template>

<script>
    export default{
        data() {
            return {
            weather:{
                cityName:"Dublin",
                country:"Ireland",
                temp: 12,
                description:"Clouds up in this",
                lowTemp:"19",
                highTemp:"27",
                feelsLike:"20",
                humidity:"55",
                icon: 10n,
                },
            }
        },

        methods: {
            getWeather: async function () {
                const weatherURL = '/weather'

                const response = await fetch(weatherURL)
                const data = await response.json()
                console.log(data);
                this.weather.temp = Math.round(data.temp);
                this.weather.description = data.rain;
                this.weather.icon = data.icon;

                // const iconURL = './assets/openweathermap-api-icons-master/icons/'+ data.icon +'.png'
                // this.weather.icon = await fetch(iconURL)
                // console.log(this.weather.icon)
            }
        },

        beforeMount(){
        this.getWeather()
        },

        
    }
</script>

<style>
@import "../assets/custom.css";
</style>