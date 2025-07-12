let tg = window.Telegram.WebApp;

tg.expand(); // Expand the app to full screen
tg.ready(); // Notify Telegram that the app is ready

function send_filters() {
  let filters = {
    is_qual: document.getElementById('is_qual').checked,
    is_amort: document.getElementById('is_amort').checked,
    is_offer: document.getElementById('is_offer').checked,
    redemption: {
      fr: parseInt(document.getElementById('redemption-from').value) * 30,
      to: parseInt(document.getElementById('redemption-to').value) * 30,
    },
    profit: {
      fr: parseInt(document.getElementById('profit-from').value),
      to: parseInt(document.getElementById('profit-to').value),
    },
    coupons: {
      fr: parseInt(document.getElementById('coupons-from').value),
      to: parseInt(document.getElementById('coupons-to').value),
    },
    duration: {
      fr: parseInt(document.getElementById('duration-from').value) * 30,
      to: parseInt(document.getElementById('duration-to').value) * 30,
    },
    sort: {
      order: Array.from(document.getElementsByClassName("order")).filter((elem) => (elem.checked)).map((elem) => (elem.value)).toString(),
      key: Array.from(document.getElementsByClassName("sort-by")).filter((elem) => (elem.checked)).map((elem) => (elem.value)).toString(),
    },
    price:  document.getElementById('price-to').value,
    rating: document.getElementById('rating-from').value,
    period: Array.from(document.getElementsByClassName("coupon-period-ckeckbox")).filter((elem) => (elem.checked)).map((elem) => parseInt(elem.value)),
    listing: Array.from(document.getElementsByClassName("listing-ckeckbox")).filter((elem) => (elem.checked)).map((elem) => parseInt(elem.value)),
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
    console.log(JSON.stringify(data))
    tg.close();
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

let btn_ok = document.getElementById("btn_ok");
btn_ok.addEventListener('click', () => {
  send_filters();
});

{
  Array.from(document.getElementsByClassName("sort-asc"), (elem, _) => elem.addEventListener('click', function() {
    document.getElementById("order-asc").checked = true;
    document.getElementById("order-dsc").checked = false;
  }));

  Array.from(document.getElementsByClassName("sort-dsc"), (elem, _) => elem.addEventListener('click', function() {
    document.getElementById("order-asc").checked = false;
    document.getElementById("order-dsc").checked = true;
  }));
}

{
  var redemptionSlider = document.getElementById('redemption-slider');
  noUiSlider.create(redemptionSlider, {
      start: [3, 36],
      connect: true,
      range: {
          'min': 0,
          'max': 120
      }
  });

  var redemptionFrom = document.getElementById('redemption-from');
  var redemptionTo = document.getElementById('redemption-to');
  var redemptions = [redemptionFrom, redemptionTo];

  redemptionSlider.noUiSlider.on('update', function (values, handle) {
    redemptions[handle].value = Math.round(values[handle]);
  });

  redemptionFrom.addEventListener('change', function () {
      redemptionSlider.noUiSlider.set([null, this.value]);
  });
  redemptionTo.addEventListener('change', function () {
      redemptionSlider.noUiSlider.set([null, this.value]);
  });
}

{
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
}

{
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
}

{
  //Слайдер дюрации
  var durationSlider = document.getElementById('duration-slider');
  noUiSlider.create(durationSlider, {
      start: [0, 50],
      connect: true,
      step: 1,
      range: {
          'min': 0,
          'max': 50
      }
  });

  var durationFrom = document.getElementById('duration-from');
  var durationTo = document.getElementById('duration-to');
  var duration = [durationFrom, durationTo];

  durationSlider.noUiSlider.on('update', function (values, handle) {
    duration[handle].value = Math.round(values[handle]*2)/2;
  });

  durationFrom.addEventListener('change', function () {
    durationSlider.noUiSlider.set([null, this.value]);
  });

  durationTo.addEventListener('change', function () {
    durationSlider.noUiSlider.set([null, this.value]);
  });
}

{
  //Слайдер цены
  var priceSlider = document.getElementById('price-slider');
  var price = document.getElementById('price-to');

  noUiSlider.create(priceSlider, {
      start: [100],
      connect: 'lower',
      step: 1,
      range: {
          'min': 0,
          'max': 200
      }
  });

  priceSlider.noUiSlider.on('update', function (value) {
    price.value = Math.round(value*2)/2;;
  });

  price.addEventListener('change', function () {
    priceSlider.noUiSlider.set([this.value]);
  });
}

{
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
}
