


// import { parse } from './module.js';

// var config = toml.parse("/opt/jbond/jbond.toml");

// $.get('/config/settings.toml', function (data) {
//   var config = toml.parse(data);
//   console.log(config);
// });


// fs.readFile('/config/settings.toml', function (err, data) {
//     var parsed = toml.parse(data);
//     console.log(parsed);
// });


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
        'max': 120
    }
});

var durationFrom = document.getElementById('duration-from');
var durationTo = document.getElementById('duration-to');
var durations = [durationFrom, durationTo];

durationSlider.noUiSlider.on('update', function (values, handle) {
  durations[handle].value = Math.round(values[handle]);
});

durationFrom.addEventListener('change', function () {
    durationSlider.noUiSlider.set([null, this.value]);
});
durationTo.addEventListener('change', function () {
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

var duratfullProfitFrom = document.getElementById('full-profit-from');
var duratfullProfitTo = document.getElementById('full-profit-to');
var fullProfits = [duratfullProfitFrom, duratfullProfitTo];

fullProfitSlider.noUiSlider.on('update', function (values, handle) {
  fullProfits[handle].value = Math.round(values[handle]*2)/2;
});

duratfullProfitFrom.addEventListener('change', function () {
  fullProfitSlider.noUiSlider.set([null, this.value]);
});
duratfullProfitTo.addEventListener('change', function () {
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

var divProfitFrom = document.getElementById('div-profit-from');
var divProfitTo = document.getElementById('div-profit-to');
var divProfits = [divProfitFrom, divProfitTo];

divProfitSlider.noUiSlider.on('update', function (values, handle) {
  divProfits[handle].value = Math.round(values[handle]*2)/2;
});

divProfitFrom.addEventListener('change', function () {
  divProfitSlider.noUiSlider.set([null, this.value]);
});

divProfitTo.addEventListener('change', function () {
  divProfitSlider.noUiSlider.set([null, this.value]);
});


//Слайдер рейтинга
var ratings = ['BB-','BB','BB+','BBB-','BBB','BBB+','A-','A','A+','AA-','AA','AA+','AAA-','AAA'];
var ratingFormat = {
  to: function(value) {
      return ratings[value];
  },
  from: function (value) {
      return ratings.indexOf(value);
  }
};

var ratingSlider = document.getElementById('rating-slider');
var ratingFrom = document.getElementById('rating-from');

noUiSlider.create(ratingSlider, {
    start: ['A-'],
    connect: 'upper',
    format: ratingFormat,
    step: 1,
    range: {
        'min': 0,
        'max': ratings.length - 1
    }
});

ratingSlider.noUiSlider.on('update', function (value) {
  ratingFrom.value = value;
});

ratingFrom.addEventListener('change', function () {
  ratingSlider.noUiSlider.set([this.value]);
});
