const API_KEY = "9cc489736a2d01b46bd10aff6d4879d4"; 

      function toggleTheme() {
            const body = document.body;
            const toggleButton = document.getElementById('mode-toggle');
            
            body.classList.toggle('light-mode');
            
           
            if (body.classList.contains('light-mode')) {
                toggleButton.innerText = '🌙'; 
                localStorage.setItem('theme', 'light');
            } else {
                toggleButton.innerText = '☀️'; 
                localStorage.setItem('theme', 'dark');
            }
        }

      let map = L.map("map", {
        zoomControl: true,
        attributionControl: false,
      }).setView([30.0444, 31.2357], 5);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
      }).addTo(map);
      let marker;

      
      const round = (v) => Math.round((v + Number.EPSILON) * 10) / 10;

      
      function showWeather(data) {
        if (!data || (data.cod && (data.cod === "404" || data.cod === 404))) {
          alert("⚠ City not found");
          return;
        }

        document.getElementById("weatherCard").classList.add("show");
        document.getElementById(
          "cityName"
        ).innerText = `${data.name} — ${data.sys.country}`;
        document.getElementById("description").innerText =
          data.weather[0].description;
        document.getElementById("temp").innerText = round(data.main.temp);
        document.getElementById("humidity").innerText = data.main.humidity;
        document.getElementById("wind").innerText = round(data.wind.speed);
        document.getElementById(
          "icon"
        ).src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@4x.png`;
        document.getElementById("icon").alt = data.weather[0].description;

        
        const alertArea = document.getElementById("rainAlertArea");
        alertArea.innerHTML = "";

        
        if (
          data.weather[0].main.toLowerCase().includes("rain") ||
          (data.rain && (data.rain["1h"] || data.rain["3h"]))
        ) {
          const div = document.createElement("div");
          div.className = "alert";
          div.textContent = "☔ Alert: Rain expected — carry an umbrella";
          alertArea.appendChild(div);
        } else {
          
          const div = document.createElement("div");
          div.className = "alert good"; 
          div.textContent = "☀️ Nice weather — enjoy your day!";
          alertArea.appendChild(div);
        }

        
        if (marker) map.removeLayer(marker);
        marker = L.marker([data.coord.lat, data.coord.lon]).addTo(map);
        map.setView([data.coord.lat, data.coord.lon], 10, { animate: true });
      }

      function showForecast(forecastData) {
        const forecastDiv = document.getElementById("forecast");
        forecastDiv.innerHTML = "";
        const daily = {};

        
        forecastData.list.forEach((item) => {
          const d = new Date(item.dt * 1000);
          
          if (d.getHours() === 12) {
            const key = d.toISOString().slice(0, 10);
            if (!daily[key]) daily[key] = item;
          }
        });

       
        if (Object.keys(daily).length < 5) {
          const seen = new Set();
          forecastData.list.forEach((item) => {
            const day = new Date(item.dt * 1000).toISOString().slice(0, 10);
            if (!seen.has(day)) {
              seen.add(day);
              daily[day] = item;
            }
          });
        }

        let i = 0;
        Object.keys(daily)
          .slice(0, 5)
          .forEach((dayKey) => {
            const it = daily[dayKey];
            const date = new Date(it.dt * 1000);
            const dayName = date.toLocaleDateString("en-US", {
              weekday: "short",
            });
            const card = document.createElement("div");
            card.className = "day-card";
            card.style.animationDelay = i * 80 + "ms"; 
            card.innerHTML = `
            <h4 style="margin:6px 0">${dayName}</h4>
            <img src="https://openweathermap.org/img/wn/${
              it.weather[0].icon
            }.png" alt="${it.weather[0].description}" />
            <div style="font-weight:700">${round(it.main.temp)}°C</div>
            <div class="muted" style="font-size:0.85rem">${
              it.weather[0].description
            }</div>
          `;
            forecastDiv.appendChild(card);
            
            setTimeout(() => card.classList.add("show"), 10 + i * 60);
            i++;
          });
      }

      function getWeatherByCity() {
        const city = document.getElementById("cityInput").value.trim();
        if (!city) {
          alert("Please enter a city name");
          return;
        }
        fetch(
          `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
            city
          )}&appid=${API_KEY}&units=metric`
        )
          .then((r) => r.json())
          .then((data) => {
            showWeather(data);
            return fetch(
              `https://api.openweathermap.org/data/2.5/forecast?q=${encodeURIComponent(
                city
              )}&appid=${API_KEY}&units=metric`
            );
          })
          .then((r) => r.json())
          .then((data) => showForecast(data))
          .catch((err) => {
            console.error(err);
            alert("⚠ Error while fetching data");
          });
      }

      function getWeatherByLocation() {
        if (!navigator.geolocation) {
          alert("⚠ Geolocation not supported");
          return;
        }
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            const lat = pos.coords.latitude,
              lon = pos.coords.longitude;
            fetch(
              `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`
            )
              .then((r) => r.json())
              .then((data) => {
                showWeather(data);
                return fetch(
                  `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`
                );
              })
              .then((r) => r.json())
              .then((data) => showForecast(data))
              .catch((err) => {
                console.error(err);
                alert("⚠ Error while fetching data");
              });
          },
          (err) => {
            console.warn(err);
            alert("⚠ Location permission denied");
          },
          { enableHighAccuracy: false, timeout: 8000 }
        );
      }

      
      function createStars(n = 150) {
        const container = document.querySelector(".stars");
        const w = window.innerWidth,
          h = window.innerHeight;
        for (let i = 0; i < n; i++) {
          const s = document.createElement("div");
          s.className = "star";
          const size = Math.random() * 2.6 + 0.6; 
          s.style.width = s.style.height = size + "px";
          s.style.left = Math.random() * w + "px";
          s.style.top = Math.random() * h + "px";
          s.style.opacity = 0.2 + Math.random() * 0.9;
          s.style.animationDuration = 2 + Math.random() * 4 + "s";
          s.style.animationDelay = Math.random() * 3 + "s";
          container.appendChild(s);
        }
      }

      
      function createMeteors(count = 20) {
        const container = document.querySelector(".meteors");
        if (!container) return;
        container.innerHTML = "";

        const w = window.innerWidth;
        const h = window.innerHeight;

        for (let i = 0; i < count; i++) {
          const m = document.createElement("div");
          m.className = "meteor";

         
          const startLeft = Math.random() * w; 
          const startTop = -(30 + Math.random() * 200); 

          m.style.left = startLeft + "px";
          m.style.top = startTop + "px";

          
          m.style.height = 60 + Math.random() * 120 + "px";
          m.style.width = 1 + Math.random() * 3 + "px";
          m.style.opacity = (0.5 + Math.random() * 0.5).toFixed(2);

          const dur = (1 + Math.random() * 30).toFixed(2); 
          const delay = (Math.random() * 6).toFixed(2); 

         
          m.style.animation = `meteorFallRightToLeft ${dur}s linear ${delay}s infinite`;

          const angle = 15 + Math.random() * 20; 
          m.style.transform = `rotate(${angle}deg)`;

          container.appendChild(m);
        }
      }

      createMeteors(16);
      getWeatherByLocation();

     
      let _t;
      window.addEventListener("resize", () => {
        clearTimeout(_t);
        _t = setTimeout(() => createMeteors(28), 250);
      });