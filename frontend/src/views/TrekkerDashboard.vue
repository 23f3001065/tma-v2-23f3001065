<template>
  <div>
    <h1>Trekker Dashboard</h1>

    <p>Welcome Trekker</p>

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