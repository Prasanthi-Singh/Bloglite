<template>
    <div class="signup-container">
  <div>
    <h2 style="text-align: center;">Sign Up</h2>
    <div class="image-container form-group" style="width:500px">
      <img :src="imageurl" v-if="imageurl">
                          <input type="file" id="upload-file" name="upload-file" @change=" onFileChange">
    </div> 
    <div class="form-group">
      <input type="text" id="name" name="name" placeholder="Enter your user_name" v-model="user_name">
    </div>
    <div class="form-group">
      <input type="email" id="email" name="email" placeholder="Enter your email" v-model="email">
    </div>
    <div class="form-group">
      <input type="password" id="password" name="password" placeholder="Enter your password" v-model="password">
    </div>
    <div class="form-group">
      <input type="text" id="name" name="confirm-password" placeholder="Bio" v-model="bio">
    </div>
    <button type="submit" class="signup-btn" v-on:click="SignUp" >Sign Up</button>
  </div>
  <div><p style="text-align: center;">If you are an existing user</p></div>
  <button style="margin-left: 42%;color: black; font-size: 10px;"><router-link to="/login" style="font-size: 15px;">Login</router-link></button>
</div>

</template>

<script>
export default{
  name:'SignUp',
  
  data(){
    return {
      email:"",
      user_name:"",
      password:"",
      bio:"",
      imageurl:"",
      fileName: 'Select Profile Photo',
    }
  },
  methods:{
    SignUp() {if (this.user_name != "" && this.email != "" && this.password != "") {
        console.log(this.user_name)
        console.log(this.email)

        fetch("http://127.0.0.1:5000/api/register", {
                  method: "POST",
                  headers: { "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    user_name: this.user_name,
                    email: this.email,
                    password: this.password,
                    bio:this.bio,
                    image:this.imageurl,
                  }),
                }).then((response)=>{
                      if (!response.ok) {
                        throw new Error('HTTP error, status code ' + response.status);
                      }
                      return response.json();
                })
                .then((data)=>{
                  console.log('yes');
                  if (data) {
                        // User registered successfully
                        localStorage.setItem("token",data.token)
                        this.$router.push( {name: 'newuser' ,query: {user_id : data.user_id }})
                      } else {
                        // Error occurred
                        throw new Error(data.description);
                      }

                }).catch((error)=>{
                  console.log("User already exist");
                  alert("User already exist")})
    }
    else{
       alert("please give all information")
     }
  },

// handleUpload(event) {
            
//         },
onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.fileName = file.name;
            const reader = new FileReader()
            reader.onload = (event) => {
                this.imageurl = event.target.result
                console.log(this.imageurl);
            }
            reader.readAsDataURL(file)
      } else {
        this.fileName = 'Select Profile Photo';
      }
    },
}
}
  //       fetch("http://127.0.0.1:5000/api/register", {
  //         method: "POST",
  //         headers: { "Content-Type": "application/json" },
  //         body: JSON.stringify({
  //           user_name: this.user_name,
  //           email: this.email,
  //           password: this.password,
  //           name:this.name,
  //           bio:this.bio,
  //         }),
  //       })
  //         .then((res) => {
  //           if (res.status === 404) {
  //             return res.json();
  //           }
  //           if (!res.ok) {
  //             throw new error("something wromng from server");
  //           }
  //           return res.json();
  //         })
  //         .then((data) => {
  //           if (data["message"] == "Provide other Username this Username already exists") {
  //             alert("This Email_id is also used, pls try different email_id");
  //           }

  //           console.log(data);
  //           localStorage.setItem("token", data.token);
  //           localStorage.setItem("user_info",  JSON.stringify(data));
  //           this.$router.push({ name: "User_details" });
  //         });
  //     } else {
  //       alert("pls give all information!!");
  //       // we will handle for all case
  //     }
  //   }
      
  //   }
  // }
</script>


<style scoped>
/* .image-container {
  width: 300px; /* set the width of the container */
  /* height: 200px; /* set the height of the container */
/* }  */

.image-container img {
  max-width: 150px; /* set the maximum width of the image to the width of its container */
 
  max-height: 100px; /* set the maximum height of the image to the height of its container */
  object-fit: contain; /* set how the image should fit within the container */
  border-radius: 50%;
  margin-left:40%}
.signup-container {
  max-width: 350px;
  margin: 0 auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 10px;
  max-width: 70%;
  margin-left: 10%;
}


input {
  font-size: 10px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.signup-btn {
  background-color: #0c0e0d;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 10px;
  margin-left: 35%;
}

.signup-btn:hover {
  background-color: #f2f7f2;
  color: #0c0e0d;
}
</style>