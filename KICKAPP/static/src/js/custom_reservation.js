odoo.define('KICKAPP.custom_reservation', function (require) {
    'use strict';

    var core = require('web.core');
    var _t = core._t;

    var unavailableDates = [];
    var reservedDates = [];

    function updateDatepicker() {
        var terrainElement = document.getElementById('terrain');
        if (!terrainElement) return;

        var terrain_id = terrainElement.value;
        fetch('/get_available_dates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ terrain_id: terrain_id })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);  // Log the received data
            unavailableDates = [];
            reservedDates = [];
            if (Array.isArray(data)) {
                data.forEach(function(event) {
                    var start = new Date(event.start);
                    var end = new Date(event.end);
                    while (start <= end) {
                        if (event.state === 'confirmed') {
                            reservedDates.push(new Date(start).toDateString());
                        } else {
                            unavailableDates.push(new Date(start).toDateString());
                        }
                        start.setDate(start.getDate() + 1);
                    }
                });
            }
            $("#date").datepicker("refresh");
        })
        .catch(error => console.error('Error:', error));
    }

    function unavailable(date) {
        var dateStr = date.toDateString();
        var today = new Date();
        today.setHours(0, 0, 0, 0); // Set to midnight to only compare dates

        if (reservedDates.includes(dateStr)) {
            return [false, "ui-state-reserved", "Reserved"];
        } else if (unavailableDates.includes(dateStr)) {
            return [false, "ui-state-unavailable", "Unavailable"];
        } else if (date < today) {
            return [false, "ui-state-disabled", "Past date"];
        } else {
            return [true, "ui-state-available", "Available"];
        }
    }

    $(document).ready(function() {
        $("#date").datepicker({
            beforeShowDay: unavailable,
            minDate: 0,
            dateFormat: 'yy-mm-dd'
        });
        $('#terrain').on('change', updateDatepicker);
        updateDatepicker();
    });
});
