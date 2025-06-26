let tg = window.Telegram.WebApp;

tg.expand(); // Expand the app to full screen
tg.ready(); // Notify Telegram that the app is ready

function send_data() {
  let filters = {
    is_qual: document.getElementById('is_qual').checked,
    is_amort: document.getElementById('is_amort').checked,
    duration: {
      // from: parseInt(document.querySelector(".duration .input .field .from").value),
      // to: parseInt(document.querySelector(".duration .input .field .to").value),

      // from: parseInt(document.getElementById('duration.from').value),
      // to: parseInt(document.getElementById('duration.to').value),
    },

    // toString() {
    //   return `{"is_qual": ${this.is_qual}, "is_amort": ${this.is_amort}}`;
    // }
  };

  document.getElementById('filters').value = JSON.stringify(filters);

  fetch("https://jbond-app.ru:8080/filters", {
    method: "POST",
    body: JSON.stringify(filters),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  });
  //.then((response) => response.json());
  //.then((json) => console.log(json));
}

// tg.MainButton.setText('Готово');
// tg.MainButton.show();
// tg.MainButton.onClick(() => {
//   send_data();
//   // tg.sendData(json);
//   tg.close();
// });


let btn_ok = document.getElementById("btn_ok");
btn_ok.addEventListener('click', () => {
  send_data();
  //tg.close();
});



//Слайдер дюрации
var durationSlider = document.getElementById('duration-slider');
noUiSlider.create(durationSlider, {
    start: [3, 36],
    connect: true,
    range: {
        'min': 0,
        'max': 100
    }
});

var duration_from = document.getElementById('duration-from');
var duration_to = document.getElementById('duration-to');
var durations = [duration_from, duration_to];

durationSlider.noUiSlider.on('update', function (values, handle) {
  durations[handle].value = Math.round(values[handle]);
});

duration_from.addEventListener('change', function () {
    durationSlider.noUiSlider.set([null, this.value]);
});
duration_to.addEventListener('change', function () {
    durationSlider.noUiSlider.set([null, this.value]);
});



// Слайдер полной доходности
var fullProfitSlider = document.getElementById('full-profit-slider');
noUiSlider.create(fullProfitSlider, {
    start: [20.0, 50.0],
    connect: true,
    range: {
        'min': 0.0,
        'max': 50.0
    }
});

var full_profit_from = document.getElementById('full-profit-from');
var full_profit_to = document.getElementById('full-profit-to');
var full_profits = [full_profit_from, full_profit_to];

fullProfitSlider.noUiSlider.on('update', function (values, handle) {
  full_profits[handle].value = Math.round(values[handle]*2)/2;
});

full_profit_from.addEventListener('change', function () {
  fullProfitSlider.noUiSlider.set([null, this.value]);
});
full_profit_to.addEventListener('change', function () {
  fullProfitSlider.noUiSlider.set([null, this.value]);
});



//Слайдер див доходности
var divProfitSlider = document.getElementById('div-profit-slider');
noUiSlider.create(divProfitSlider, {
    start: [20.0, 50.0],
    connect: true,
    range: {
        'min': 0.0,
        'max': 50.0
    }
});

var div_profit_from = document.getElementById('div-profit-from');
var div_profit_to = document.getElementById('div-profit-to');
var div_profits = [div_profit_from, div_profit_to];

divProfitSlider.noUiSlider.on('update', function (values, handle) {
  div_profits[handle].value = Math.round(values[handle]*2)/2;
});

div_profit_from.addEventListener('change', function () {
  divProfitSlider.noUiSlider.set([null, this.value]);
});

div_profit_to.addEventListener('change', function () {
  divProfitSlider.noUiSlider.set([null, this.value]);
});
