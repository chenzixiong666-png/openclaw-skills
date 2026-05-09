UPDATE weather_station_build_test
SET Weather_desc = 'Cloudy',
    Extreme_weather_desc = '无',
    Max_temp = '21°C',
    Min_temp = '17°C',
    App_temp = '19°C',
    Rh = '90%',
    Pop = '80%',
    Wind_spd = '2m/s',
    Wind_dir = 'SW',
    Uv = 3,
    Vis = '20km',
    Pm10 = '120μg/m3',
    Pm25 = '60μg/m3',
    So2 = '60μg/m3',
    No2 = '200μg/m3',
    Co = '800μg/m3',
    O3 = '60μg/m3',
    yesterday_weather = '{"weatherDesc":"rain","maxTemp":21,"minTemp":17,"appTemp":20}',
    indoor = '{"temperature":"20","humidity":"40"}',
    Pollen = 0,
    Mold = 2
WHERE ID = 3021;

SELECT * FROM weather_station_build_test WHERE ID = 3021;
