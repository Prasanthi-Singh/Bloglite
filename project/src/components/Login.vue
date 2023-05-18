<template>
  <div>
    <div class="login-container">
      <h1>Login</h1>
      <div>
        <label for="user_name">User_name</label>
        <input type="text" v-model="user_name" required>
        <label for="password">Password</label>
        <input type="password" v-model="password" required>
        <button type="submit" class="aq" v-on:click="Login">Login</button>
        <div style="margin-top: 5%; margin-bottom: 2%;">If you are a new user</div>
        <div><button class="aq" style="background-color:white;border: black 2px;"><RouterLink to="/" style="font-size: 14px;">SignUp</RouterLink></button></div>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'Login',
  data() {
    return {
      user_name: "",
      password: ""
    }
  },
  methods: {
    Login() {
      //   console.log(new FormData(document.querySelector("#login").entries));
      if (this.user_name == "" || this.password == "") {
        // this.$router.push({ name: "login" });
        alert("Please Provide all the Information");
      } else {
        console.log(this.user_name)
        fetch("http://127.0.0.1:5000/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({

            user_name: this.user_name,
            password: this.password,
          }),
        }).then((response) => {
          if (!response.ok) {
            throw new Error('HTTP error, status code ' + response.status);
          }
          return response.json();
        })
          .then((data) => {
            console.log(data),
            localStorage.setItem("token",data.token)
              this.$router.push({ name: 'Profile', query: { user_id: data.user_id } })

          })
          .catch((error) => {
            console.log(error);
            alert('Provide Correct Credentials')
          })
      }
    },
    
  }
}
</script>
  
<style>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.8rem;
  margin-bottom: 1rem;
  border: 5px;
  border-radius: 0.5rem;
}

.aq {
  padding: 0.8rem 1.5rem;
  background-color: #060606;
  color: #f5f0f0
  ;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}</style>
  