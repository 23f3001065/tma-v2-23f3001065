<template>

<div class="container mt-4">

    <h1>Trekker Dashboard</h1>

    <p>

        Welcome, <b>{{ user.name }}</b>

    </p>

    <button
        class="btn btn-danger mb-4"
        @click="logout">

        Logout

    </button>

  <button
      class="btn btn-primary mb-4 ms-2"
      @click="exportHistory">

      Export Booking History

  </button>

    <input
        class="form-control mb-3"
        type="text"
        placeholder="Search by name, location or difficulty"
        v-model="search">

    <h3>

        Available Treks

    </h3>

    <div
        class="card mb-3"
        v-for="trek in filteredTreks"
        :key="trek.id">

        <div class="card-body">

            <h4>

                {{ trek.name }}

            </h4>

            <p>

                Location :
                {{ trek.location }}

            </p>

            <p>

                Difficulty :
                {{ trek.difficulty }}

            </p>

            <p>

                Status :
                {{ trek.status }}

            </p>

            <p>

                Slots :
                {{ trek.available_slots }}

            </p>

            <button
                class="btn btn-primary me-2"
                @click="viewDetails(trek.id)">

                View Details

            </button>

            <button
                v-if="!bookedTrekIds.includes(trek.id)"
                class="btn btn-success"
                @click="bookTrek(trek.id)">

                Book Trek

            </button>

            <button
                v-else
                class="btn btn-secondary"
                disabled>

                Already Booked

            </button>

            <div
                v-if="selectedTrek && selectedTrek.id === trek.id"
                class="border rounded p-3 mt-3 bg-light">

                <h5>Trek Details</h5>

                <p>
                    <strong>Location:</strong>
                    {{ selectedTrek.location }}
                </p>

                <p>
                    <strong>Difficulty:</strong>
                    {{ selectedTrek.difficulty }}
                </p>

                <p>
                    <strong>Duration:</strong>
                    {{ selectedTrek.duration_days }} days
                </p>

                <p>
                    <strong>Description:</strong>
                    {{ selectedTrek.description }}
                </p>

                <p>
                    <strong>Available Slots:</strong>
                    {{ selectedTrek.available_slots }}
                </p>

                <p>
                    <strong>Start Date:</strong>
                    {{ selectedTrek.start_date }}
                </p>

                <p>
                    <strong>End Date:</strong>
                    {{ selectedTrek.end_date }}
                </p>

                <hr>

            </div>

        </div>

    </div>

    <h3 class="mt-5">

        My Bookings

    </h3>

    <div
        class="card mb-3"
        v-for="booking in bookings"
        :key="booking.id">

        <div class="card-body">

            <h4>

                {{ booking.trek_name }}

            </h4>

            <p>

                Location :
                {{ booking.location }}

            </p>

            <p>

                Booking Date :
                {{ booking.booking_date }}

            </p>

            <p>

                Status :
                {{ booking.status }}

            </p>
            <button
                v-if="booking.status == 'Booked'"
                class="btn btn-danger"
                @click="cancelBooking(booking.id)">

                Cancel Booking

            </button>

        </div>

    </div>

</div>

</template>

<script>
import axios from 'axios'

export default {

  data() {

    return {

      user: {},

      treks: [],
      bookings: [],
      selectedTrek: null,
      search: ''

    }

  },

  methods: {

    logout() {

      localStorage.clear()

      this.$router.replace('/login')

    },

    async fetchProfile() {

        const token = localStorage.getItem('token')

        const response = await axios.get(

            'http://127.0.0.1:5000/trekker/profile',

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        )

        this.user = response.data

    },

    async fetchTreks() {

      const token = localStorage.getItem('token')

      const response = await axios.get(

        'http://127.0.0.1:5000/treks',

        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }

      )

      this.treks = response.data

    },

    async fetchBookings() {

        const token = localStorage.getItem('token')

        const response = await axios.get(

            'http://127.0.0.1:5000/bookings',

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        )

        this.bookings = response.data

    },

    async viewDetails(trekId) {

        if (
            this.selectedTrek &&
            this.selectedTrek.id == trekId
        ) {

            this.selectedTrek = null
            return

        }

        const token = localStorage.getItem('token')

        const response = await axios.get(

            `http://127.0.0.1:5000/treks/${trekId}`,

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        )

        this.selectedTrek = response.data

    },

    async bookTrek(trekId) {

        const token = localStorage.getItem('token')

        try {

            const response = await axios.post(

                'http://127.0.0.1:5000/bookings',

                {
                    trek_id: trekId
                },

                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }

            )

            alert(response.data.msg)

            await this.fetchTreks()

            await this.fetchBookings()

        }

        catch (error) {

            alert(
                error.response.data.msg
            )

        }

    },

    async cancelBooking(bookingId) {

        const token = localStorage.getItem('token')

        try {

            const response = await axios.delete(

                `http://127.0.0.1:5000/bookings/${bookingId}`,

                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }

            )

            alert(response.data.msg)

            await this.fetchBookings()

            await this.fetchTreks()

        }

        catch (error) {

            alert(
                error.response.data.msg
            )

        }

    },

    async exportHistory() {

        const token = localStorage.getItem('token')

        const response = await axios.put(

            'http://127.0.0.1:5000/bookings',

            {},

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        )

        alert(response.data.msg)

    }

  },

  computed: {

      filteredTreks() {

          return this.treks.filter((trek) => {

              const text = this.search.toLowerCase()

              return (

                  trek.name.toLowerCase().includes(text) ||

                  trek.location.toLowerCase().includes(text) ||

                  trek.difficulty.toLowerCase().includes(text)

              )

          })

      },

      bookedTrekIds() {

          return this.bookings
              .filter(booking => booking.status == 'Booked')
              .map(booking => booking.trek_id)

      },

  },
  
  mounted() {

    this.fetchProfile()
    this.fetchTreks()
    this.fetchBookings()

  }

}
</script>