<template>
  <div>

    <h1>Register</h1>

    <form @submit.prevent="registerUser">

      <div>
        <label>Name</label>
        <input
          type="text"
          v-model="name"
        />
      </div>

      <br>

      <div>
        <label>Email</label>
        <input
          type="email"
          v-model="email"
        />
      </div>

      <br>

      <div>
        <label>Password</label>
        <input
          type="password"
          v-model="password"
        />
      </div>

      <br>

      <button type="submit">
        Register
      </button>

    </form>

    <p>
        Already have an account?
        <router-link to="/login">
            Login
        </router-link>
    </p>

    <p>{{ message }}</p>

  </div>
</template>

<script>
import axios from 'axios'

export default {

  data() {
    return {
      name: '',
      email: '',
      password: '',
      message: ''
    }
  },

  methods: {

    async registerUser() {

      try {

        const response = await axios.post(
          'http://127.0.0.1:5000/auth/register',
          {
            name: this.name,
            email: this.email,
            password: this.password
          }
        )

        this.message = response.data.msg

        this.name = ''
        this.email = ''
        this.password = ''

      }

      catch (error) {

        if (error.response) {
          this.message = error.response.data.msg
        }

        else {
          this.message = 'Server error'
        }

      }

    }

  }

}
</script>