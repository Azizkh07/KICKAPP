odoo.define('KICKAPP.ReservationComponent', function (require) {
    'use strict';

    const { Component } = owl;

    class ReservationComponent extends Component {
        async willStart() {
            this.terrainId = null;
            this.availableDates = [];
            this.reservedDates = [];
            await this.fetchAvailableDates();
        }

        async fetchAvailableDates() {
            try {
                const response = await this.rpc('/get_available_dates', { terrain_id: this.terrainId });
                this.availableDates = response.available_dates;
                this.reservedDates = response.reserved_dates;
            } catch (error) {
                console.error('Error fetching available dates:', error);
            }
        }

        async onTerrainChange(ev) {
            this.terrainId = ev.target.value;
            await this.fetchAvailableDates();
        }
    }



    return ReservationComponent;
});
