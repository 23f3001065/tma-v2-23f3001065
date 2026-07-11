<template>

<div class="container mt-4">

    <h1>Staff Dashboard</h1>

    <p>Welcome, <b>{{ staff.name }}</b></p>

    <button
        class="btn btn-danger mb-4"
        @click="logout">

        Logout

    </button>

    <h3>Assigned Treks</h3>

    <div
        class="card mb-3"
        v-for="trek in treks"
        :key="trek.id">

        <div class="card-body">

            <h4>{{ trek.name }}</h4>

            <p>

                Trek ID :
                {{ trek.id }}

            </p>

            <p>

                Status :
                {{ trek.status }}

            </p>

            <button class="btn btn-primary me-2"
            @click="viewDetails(trek.id)">

                View Details

            </button>

            <button class="btn btn-warning me-2"
            @click="showUpdateForm(trek)">

                Update

            </button>

            <button class="btn btn-secondary">

                View Reg. Users

            </button>

            <div
                v-if="selectedTrek === trek.id"
                class="mt-3">

                <input
                    class="form-control mb-2"
                    type="number"
                    v-model="updateForm.available_slots"
                    placeholder="Available Slots">

                <select
                    class="form-select mb-2"
                    v-model="updateForm.status">

                    <option>Pending</option>
                    <option>Open</option>
                    <option>Closed</option>
                    <option>Completed</option>

                </select>

                <button
                    class="btn btn-success"
                    @click="updateTrek(trek.id)">

                    Save

                </button>

            </div>

            <div
                v-if="selectedTrekDetails && selectedTrekDetails.id === trek.id"
                class="border rounded p-3 mt-3 bg-light">

                <h5>Trek Details</h5>

                <p>
                    <strong>Location:</strong>
                    {{ selectedTrekDetails.location }}
                </p>

                <p>
                    <strong>Difficulty:</strong>
                    {{ selectedTrekDetails.difficulty }}
                </p>

                <p>
                    <strong>Duration:</strong>
                    {{ selectedTrekDetails.duration_days }} days
                </p>

                <p>
                    <strong>Description:</strong>
                    {{ selectedTrekDetails.description }}
                </p>

                <p>
                    <strong>Available Slots:</strong>
                    {{ selectedTrekDetails.available_slots }}
                </p>

                <p>
                    <strong>Start Date:</strong>
                    {{ selectedTrekDetails.start_date }}
                </p>

                <p>
                    <strong>End Date:</strong>
                    {{ selectedTrekDetails.end_date }}
                </p>

            </div>
            
        </div>

    </div>

</div>

</template>

<script>
import axios from 'axios'

export default {

  data() {
    return {
      staff: {},

      treks: [],
      selectedTrek: null,
      selectedTrekDetails: null,

      updateForm: {
        available_slots: 0,
        status: ''
      }
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

        'http://127.0.0.1:5000/staff/profile',

        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }

      )

      this.staff = response.data

    },

    async fetchTreks() {

      const token = localStorage.getItem('token')

      const response = await axios.get(
        'http://127.0.0.1:5000/staff/treks',
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      this.treks = response.data

    },   

    async viewDetails(trekId) {

      if (
        this.selectedTrekDetails &&
        this.selectedTrekDetails.id === trekId
      ) {
        this.selectedTrekDetails = null
        return
      }

      const token = localStorage.getItem('token')

      const response = await axios.get(
        `http://127.0.0.1:5000/staff/treks/${trekId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      this.selectedTrekDetails = response.data

    },

    showUpdateForm(trek) {

      this.selectedTrek = trek.id

      this.selectedTrekDetails = null

      this.updateForm.available_slots = trek.available_slots

      this.updateForm.status = trek.status

    },

    async updateTrek(trekId) {

      const token = localStorage.getItem('token')

      await axios.put(

        `http://127.0.0.1:5000/staff/treks/${trekId}`,

        this.updateForm,

        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }

      )
      
      const response = await axios.get(
        `http://127.0.0.1:5000/staff/treks/${trekId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      this.selectedTrekDetails = response.data

      if (
        this.selectedTrekDetails &&
        this.selectedTrekDetails.id === trekId
      ) {
        await this.viewDetails(trekId)
      }

      await this.fetchTreks()
      this.selectedTrek = null

      this.fetchTreks()

    },

  },

  mounted() {

    this.fetchProfile()
    this.fetchTreks()

  }

}
</script>