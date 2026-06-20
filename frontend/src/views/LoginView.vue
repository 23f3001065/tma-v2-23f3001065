<template>
  <div>

    <h1>Login</h1>

    <form @submit.prevent="loginUser">

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
        Login
      </button>

    </form>

    <p>{{ message }}</p>

  </div>
</template>

<script>
import axios from 'axios'

export default {

  data() {
    return {
      email: '',
      password: '',
      message: ''
    }
  },

  methods: {

    async loginUser() {

      try {

        const response = await axios.post(
          'http://127.0.0.1:5000/auth/login',
          {
            email: this.email,
            password: this.password
          }
        )

        localStorage.setItem(
          'token',
          response.data.access_token
        )

        localStorage.setItem(
          'role',
          response.data.role
        )

        this.message = response.data.msg

        if (response.data.role === 'admin') {
            this.$router.push('/admin-dashboard')
        }

        else if (response.data.role === 'staff') {
            this.$router.push('/staff-dashboard')
        }

        else {
            this.$router.push('/trekker-dashboard')
        }

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