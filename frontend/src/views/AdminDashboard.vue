<template>
  <div>

    <h1>Admin Dashboard</h1>

    <button @click="logout">
      Logout
    </button>

    <hr>

    <h2>Dashboard Statistics</h2>

    <p>Total Users: {{ stats.total_users }}</p>

    <p>Total Staff: {{ stats.total_staff }}</p>

    <p>Total Treks: {{ stats.total_treks }}</p>

    <p>Total Bookings: {{ stats.total_bookings }}</p>

    <hr>

    <h2>Create Trek</h2>

    <form @submit.prevent="createTrek">

      <div>
        <label>Name</label>
        <input
          type="text"
          v-model="name"
        >
      </div>

      <br>

      <div>
        <label>Location</label>
        <input
          type="text"
          v-model="location"
        >
      </div>

      <br>

      <div>
        <label>Difficulty</label>
        <input
          type="text"
          v-model="difficulty"
        >
      </div>

      <br>

      <div>
        <label>Duration Days</label>
        <input
          type="number"
          v-model="duration_days"
        >
      </div>

      <br>

      <div>
        <label>Description</label>
        <input
          type="text"
          v-model="description"
        >
      </div>

      <br>

      <div>
        <label>Available Slots</label>
        <input
          type="number"
          v-model="available_slots"
        >
      </div>

      <br>

      <div>
        <label>Start Date</label>
        <input
          type="date"
          v-model="start_date"
        >
      </div>

      <br>

      <div>
        <label>End Date</label>
        <input
          type="date"
          v-model="end_date"
        >
      </div>

      <br>

      <button type="submit">
        Create Trek
      </button>

    </form>

    <p>{{ message }}</p>

    <hr>

    <h2>Search Trek</h2>

    <input
        type="text"
        placeholder="Search by Trek Name or ID"
        v-model="trekSearch"
    >

    <br>

    <h2>All Treks</h2>

    <div
        v-for="trek in filteredTreks"
        :key="trek.id"
    >

        <h3>{{ trek.name }}</h3>

        <p>

            Trek ID :
            {{ trek.id }}

        </p>

        <button
            @click="viewDetails(trek.id)"
        >

            {{
                showDetails === trek.id
                ? 'Hide Details'
                : 'View Details'
            }}

        </button>

        <button
            @click="editDetails(trek)"
        >

            Edit

        </button>

        <button
            @click="deleteTrek(trek.id)"
        >

            Delete

        </button>

        <br>

        <div
            v-if="showDetails === trek.id"
        >

            <p>

                Location :
                {{ trek.location }}

            </p>

            <p>

                Difficulty :
                {{ trek.difficulty }}

            </p>

            <p>

                Duration :
                {{ trek.duration_days }}

            </p>

            <p>

                Slots :
                {{ trek.available_slots }}

            </p>

            <p>

                Status :
                {{ trek.status }}

            </p>

            <p>

              Assigned Staff:
              {{ trek.staff_name || 'Not Assigned' }}
            
            </p>

        </div>

        <div
            v-if="showEdit === trek.id"
        >

            <hr>

            <h4>Edit Trek</h4>

            <div>

                <label>Name</label>

                <input
                    type="text"
                    v-model="editTrek.name"
                >

            </div>

            <br>

            <div>

                <label>Location</label>

                <input
                    type="text"
                    v-model="editTrek.location"
                >

            </div>

            <br>

            <div>

                <label>Difficulty</label>

                <input
                    type="text"
                    v-model="editTrek.difficulty"
                >

            </div>

            <br>

            <button
                @click="updateTrek(editTrek)"
            >

                Save Changes

            </button>

            <button
                @click="cancelEdit"
            >

                Cancel

            </button>

        </div>

        <hr>

    </div>

    <hr>

    <h2>Staff Management</h2>

    <form
        @submit.prevent="createStaff"
    >

        <div>

            <label>Name</label>

            <input
                type="text"
                v-model="staffName"
            >

        </div>

        <br>

        <div>

            <label>Email</label>

            <input
                type="email"
                v-model="staffEmail"
            >

        </div>

        <br>

        <div>

            <label>Password</label>

            <input
                type="password"
                v-model="staffPassword"
            >

        </div>

        <br>

        <button
            type="submit"
        >

            Create Staff

        </button>

    </form>

    <hr>

    <h2>Assign Staff To Trek</h2>

    <div>

        <label>Select Trek</label>

        <select
            v-model="selectedTrek"
        >

            <option
                disabled
                value=""
            >
                Select Trek
            </option>

            <option
                v-for="trek in treks"
                :key="trek.id"
                :value="trek.id"
            >

                {{ trek.name }}

            </option>

        </select>

    </div>

    <br>

    <div>

        <label>Select Staff</label>

        <select
            v-model="selectedStaff"
        >

            <option
                disabled
                value=""
            >
                Select Staff
            </option>

            <option
                v-for="staffMember in staff"
                :key="staffMember.id"
                :value="staffMember.id"
            >

                {{ staffMember.name }}

            </option>

        </select>

    </div>

    <br>

    <button
        @click="assignStaff"
    >

        Assign Staff

    </button>

    <hr>

    <h2>Search User</h2>

    <input
        type="text"
        placeholder="Search by Name, Email or ID"
        v-model="userSearch"
    >

    <br>

    <h2>All Users</h2>

    <div
        v-for="user in filteredUsers"
        :key="user.id"
    >

        <h3>

            {{ user.name }}

        </h3>

        <p>

            ID :
            {{ user.id }}

        </p>

        <p>

            {{ user.email }}

        </p>

        <p>

            Role :
            {{ user.role }}

        </p>

        <p>

            Status :

            {{ user.is_active ? 'Active' : 'Inactive' }}

        </p>

        <button

            v-if="user.role !== 'admin'"

            @click="toggleUserStatus(user)"

        >

            {{ user.is_active ? 'Deactivate' : 'Activate' }}

        </button>

        <hr>

    </div>

  </div>
</template>

<script>

import axios from 'axios'

export default {

  data() {
    return {

      stats: {},

      treks: [],
      trekSearch: '',

      users: [],
      userSearch: '',

      staff: [],

      showDetails: null,
      showEdit: null,
      editTrek: {},

      staffName: '',
      staffEmail: '',
      staffPassword: '',

      name: '',
      location: '',
      difficulty: '',
      duration_days: '',
      description: '',
      available_slots: '',
      start_date: '',
      end_date: '',

      selectedTrek: '',
      selectedStaff: '',

      message: ''

    }
  },

  async mounted() {

    await this.fetchDashboard()

    await this.fetchTreks()

    await this.fetchUsers()

  },

  computed: {

      filteredTreks() {

          return this.treks.filter(trek =>

              trek.name
                  .toLowerCase()
                  .includes(
                      this.trekSearch.toLowerCase()
                  )

              ||

              trek.id
                  .toString()
                  .includes(this.trekSearch)

          )

      },

      filteredUsers() {

          return this.users.filter(user =>

              user.name
                  .toLowerCase()
                  .includes(
                      this.userSearch.toLowerCase()
                  )

              ||

              user.email
                  .toLowerCase()
                  .includes(
                      this.userSearch.toLowerCase()
                  )

              ||

              user.id
                  .toString()
                  .includes(this.userSearch)

          )

      }

  },

  methods: {

    async fetchDashboard() {

        try {

            const token =
                localStorage.getItem('token')

            const response =
                await axios.get(
                    'http://127.0.0.1:5000/admin/dashboard',
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            this.stats = response.data

        }

        catch (error) {

            if (
                this.handleUnauthorized(error)
            ) {

                return

            }

            console.log(error)

        }

    },

    handleUnauthorized(error) {

        if (
            error.response &&
            error.response.status === 401
        ) {

            localStorage.removeItem('token')

            localStorage.removeItem('role')

            alert(
                'Session expired. Please login again.'
            )

            this.$router.push('/login')

            return true

        }

        return false

    },    

    async fetchTreks() {

      const token =
        localStorage.getItem('token')

      const response =
        await axios.get(
          'http://127.0.0.1:5000/admin/treks',
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

      this.treks = response.data

    },

    async createTrek() {

      try {

        const token =
          localStorage.getItem('token')

        const response =
          await axios.post(
            'http://127.0.0.1:5000/admin/treks',

            {
              name: this.name,
              location: this.location,
              difficulty: this.difficulty,
              duration_days: this.duration_days,
              description: this.description,
              available_slots: this.available_slots,
              start_date: this.start_date,
              end_date: this.end_date
            },

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        this.message =
          response.data.msg

        alert(this.message)

        this.name = ''
        this.location = ''
        this.difficulty = ''
        this.duration_days = ''
        this.description = ''
        this.available_slots = ''
        this.start_date = ''
        this.end_date = ''

        await this.fetchTreks()

        await this.fetchDashboard()

      }

      catch (error) {

          if (error.response) {

              this.message =
                  error.response.data.msg

          }

          else {

              this.message =
                  'Server error'

          }

          alert(this.message)

      }

    },

    viewDetails(trekId) {

        if (this.showDetails === trekId) {
            this.showDetails = null
        }

        else {
            this.showDetails = trekId
        }
    },

    editDetails(trek) {
        this.showEdit = trek.id
        this.editTrek = {
            id: trek.id,
            name: trek.name,
            location: trek.location,
            difficulty: trek.difficulty
        }
    },

    cancelEdit() {
        this.showEdit = null
    },    

    async updateTrek(trek) {
      try {
        const token =
          localStorage.getItem('token')
        const response =
          await axios.put(
            `http://127.0.0.1:5000/admin/treks/${trek.id}`,
            {
              name: trek.name,
              location: trek.location,
              difficulty: trek.difficulty
            },

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        this.message =
          response.data.msg

        alert(this.message)

        await this.fetchTreks()
        await this.fetchDashboard()

        this.showEdit = null

      }

      catch (error) {

          if (error.response) {

              this.message =
                  error.response.data.msg

          }

          else {

              this.message =
                  'Server error'

          }

          alert(this.message)

      }

    },

    async deleteTrek(trekId) {

      if (!confirm('Delete this trek?')) {

    return
    }

      try {

        const token =
          localStorage.getItem('token')

        const response =
          await axios.delete(

            `http://127.0.0.1:5000/admin/treks/${trekId}`,

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }

          )

        this.message =
          response.data.msg

        alert(this.message)

        await this.fetchTreks()

        await this.fetchDashboard()

      }

      catch (error) {

        if (error.response) {

          this.message =
            error.response.data.msg

        }

        else {

            this.message =
                'Server error'

        }

        alert(this.message)

      }

    },

    async fetchUsers() {

        const token =
            localStorage.getItem('token')

        const response =
            await axios.get(

                'http://127.0.0.1:5000/admin/users',

                {
                    headers: {
                        Authorization:
                            `Bearer ${token}`
                    }
                }

            )

        this.users = response.data

        this.staff = this.users.filter(
            user => user.role === 'staff'
        )        

    },

    async createStaff() {

        try {

            const token =
                localStorage.getItem('token')

            const response =
                await axios.post(

                    'http://127.0.0.1:5000/admin/users',

                    {

                        name: this.staffName,

                        email: this.staffEmail,

                        password: this.staffPassword

                    },

                    {

                        headers: {

                            Authorization:
                                `Bearer ${token}`

                        }

                    }

                )

            this.message =
                response.data.msg

            alert(this.message)

            this.staffName = ''

            this.staffEmail = ''

            this.staffPassword = ''

            await this.fetchUsers()

            await this.fetchDashboard()

        }

        catch (error) {

            if (error.response) {

                this.message = error.response.data.msg
                alert(this.message)

            }

            else {

                this.message = 'Server error'
                alert(this.message)

            }

        }
      },

async toggleUserStatus(user) {

    const action =
        user.is_active
            ? 'Deactivate'
            : 'Activate'

    if (
        !confirm(`${action} this user?`)
    ) {

        return

    }

    try {

        const token =
            localStorage.getItem('token')

        const response =
            await axios.put(

                `http://127.0.0.1:5000/admin/users/${user.id}`,

                {
                    is_active:
                        !user.is_active
                },

                {
                    headers: {
                        Authorization:
                            `Bearer ${token}`
                    }
                }

            )

        this.message =
            response.data.msg

        alert(this.message)

        await this.fetchUsers()

        await this.fetchDashboard()

    }

    catch (error) {

        if (error.response) {

            this.message =
                error.response.data.msg

        }

        else {

            this.message =
                'Server error'

        }

        alert(this.message)

    }

},

    async assignStaff() {

        if (!this.selectedTrek) {

            alert('Please select a trek')

            return

        }

        if (!this.selectedStaff) {

            alert('Please select a staff member')

            return

        }

        try {

            const token =
                localStorage.getItem('token')

            const response =
                await axios.put(

                    `http://127.0.0.1:5000/admin/treks/${this.selectedTrek}/assign-staff`,

                    {
                        staff_id: this.selectedStaff
                    },

                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }

                )

            this.message =
                response.data.msg

            alert(this.message)

            this.selectedTrek = ''

            this.selectedStaff = ''

            await this.fetchTreks()

            await this.fetchDashboard()

        }

        catch (error) {

            if (error.response) {

                this.message =
                    error.response.data.msg

            }

            else {

                this.message =
                    'Server error'

            }

            alert(this.message)

        }

    },

    logout() {

      localStorage.removeItem('token')

      localStorage.removeItem('role')

      this.$router.push('/login')

    }

  }

}
</script>