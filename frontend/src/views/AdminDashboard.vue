<template>
  <div>

    <h1>Admin Dashboard</h1>

    <p>Welcome Admin</p>

    <button @click="logout">
      Logout
    </button>

  </div>
</template>

<script>
export default {

  methods: {

    logout() {

      localStorage.removeItem('token')
      localStorage.removeItem('role')

      this.$router.push('/login')

    }

  }

}
</script>