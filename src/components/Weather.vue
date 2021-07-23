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
                icon: 10n,
                },
            }
        },

        methods: {
            getWeather: async function () {
                const weatherURL = '/weather'
                const response = await fetch(weatherURL)
                const data = await response.json()
                this.weather.temp = Math.round(data.temp);
                this.weather.description = data.rain;
                this.weather.icon = data.icon;

            }
        },

        beforeMount(){
        this.getWeather()
        },

        
    }
</script>

<style scoped>
#main {
position: absolute;
height: 100%;
width: 100%;
}

.day {
background: linear-gradient(to bottom left, #d7d3ac, #ffffff);
}
.night {
background: linear-gradient(to bottom left, #4854a2, #3d3d3d);
color: white;
}

.title {
font-size: 50px;
font-weight: 500;
}

.form-rounded {
border-radius: 2rem;
}
.back-card {
border-radius: 40px !important;
color: white;
background: linear-gradient(to bottom right, #707070, #434647);
text-shadow: 2px 2px 2px #707070;
}

.city-name {
position: absolute;
width: 100%;
}

.city-name p {
font-weight: 400;
font-size: 16pt;
}

.city-name span {
position: relative;
top: -50px;
font-size: 40pt;
font-family: "Times New Roman", Times, serif;
}

.temp span {
font-weight: 100;
font-size: 5em;
letter-spacing: -5px;
white-space: nowrap;
}
.card-mid {
line-height: 0.1;
}
.condition {
font-size: 1em;
font-weight: 700;
line-height: 1em;
text-transform: capitalize;
}

.high {
font-size: 15px;
}

.low {
font-size: 15px;
}

.card-bottom p {
font-size: 50px;
font-weight: 100;
letter-spacing: -3px;
}
.card-bottom {
line-height: 0.5;
}

.card-bottom span {
font-size: 12px;
}

.form-control:focus {
box-shadow: none;
border-color: inherit;
}
</style>