<template>
  <div>

    <h1>Available Treks</h1>

    <div v-for="trek in treks" :key="trek.id">

      <h3>{{ trek.name }}</h3>

      <p>Location: {{ trek.location }}</p>

      <p>Difficulty: {{ trek.difficulty }}</p>

      <p>Duration: {{ trek.duration_days }} days</p>

      <p>Slots: {{ trek.available_slots }}</p>

      <p>Status: {{ trek.status }}</p>

      <hr>

    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {

  data() {
    return {
      treks: []
    }
  },

  async mounted() {

    try {

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

    }

    catch (error) {

      console.log(error)

    }

  }

}
</script>