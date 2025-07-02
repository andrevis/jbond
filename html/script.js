let tg = window.Telegram.WebApp;

tg.expand(); // Expand the app to full screen
tg.ready(); // Notify Telegram that the app is ready

function send_filters() {

  let filters = {
    is_qual: document.getElementById('is_qual').checked,
    is_amort: document.getElementById('is_amort').checked,
    duration: {
      fr: parseInt(document.getElementById('duration-from').value),
      to: parseInt(document.getElementById('duration-to').value),
    },
    profit: {
      fr: parseInt(document.getElementById('profit-from').value),
      to: parseInt(document.getElementById('profit-to').value),
    },
    coupons: {
      fr: parseInt(document.getElementById('coupons-from').value),
      to: parseInt(document.getElementById('coupons-to').value),
    },
    rating: document.getElementById('rating-from').value,
    period: Array.from(document.getElementsByClassName("coupon-period-ckeckbox")).map((elem) => parseInt(elem.value)),
    chat_id: tg.initDataUnsafe.user.id
  };

  document.getElementById('filters').value = JSON.stringify(filters);

  fetch("https://jbond-app.ru:8080/filters", {
    method: "POST",
    body: JSON.stringify(filters),
    headers: {
      "Content-type": "application/json"
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    document.getElementById('data').value = JSON.stringify(data);

  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// tg.MainButton.setText('Готово');
// tg.MainButton.show();
// tg.MainButton.onClick(() => {
//   send_filters();
//   // tg.sendData(json);
//   tg.close();
// });


let btn_ok = document.getElementById("btn_ok");
btn_ok.addEventListener('click', () => {
  send_filters();
  // tg.sendData(tg.initDataUnsafe.user.id.toString());

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



// Слайдер доходности
var profitSlider = document.getElementById('profit-slider');
noUiSlider.create(profitSlider, {
    start: [20.0, 50.0],
    connect: true,
    range: {
        'min': 0.0,
        'max': 50.0
    }
});

var profitFrom = document.getElementById('profit-from');
var profitTo = document.getElementById('profit-to');
var profits = [profitFrom, profitTo];

profitSlider.noUiSlider.on('update', function (values, handle) {
  profits[handle].value = Math.round(values[handle]*2)/2;
});

profitFrom.addEventListener('change', function () {
  profitSlider.noUiSlider.set([null, this.value]);
});
profitTo.addEventListener('change', function () {
  profitSlider.noUiSlider.set([null, this.value]);
});



//Слайдер див доходности
var couponsSlider = document.getElementById('coupons-slider');
noUiSlider.create(couponsSlider, {
    start: [20.0, 50.0],
    connect: true,
    range: {
        'min': 0.0,
        'max': 50.0
    }
});

var couponsFrom = document.getElementById('coupons-from');
var couponsTo = document.getElementById('coupons-to');
var coupons = [couponsFrom, couponsTo];

couponsSlider.noUiSlider.on('update', function (values, handle) {
  coupons[handle].value = Math.round(values[handle]*2)/2;
});

couponsFrom.addEventListener('change', function () {
  couponsSlider.noUiSlider.set([null, this.value]);
});

couponsTo.addEventListener('change', function () {
  couponsSlider.noUiSlider.set([null, this.value]);
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
