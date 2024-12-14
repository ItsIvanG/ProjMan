<template>
  <div class="user-profile">
    <form @submit.prevent="handleSubmit">
      <!-- Aligned Containers: Profile and Email/Name -->
      <div class="aligned-container">
        <!-- Profile Container -->
        <div class="box-container profile-container">
          <h1>Profile Photo</h1>
          <h4>Set a new profile picture for your account.</h4>
          <div class="profile-picture-container" @click="triggerFileInput">
            <img
              v-if="user.profilePicture"
              :src="user.profilePicture"
              alt="Profile Preview"
              class="profile-picture"
            />
            <span v-else class="person-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#101010" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4z"/><path d="M20 20c0-4.42-3.58-8-8-8s-8 3.58-8 8"/></svg>
            </span>
            <input type="file" id="profile-picture" @change="handleFileChange" hidden />
          </div>

          <!-- Username Display -->
           <div class="username-display">
             <input
                 type="text"
                 v-model="user.username"
                 placeholder="@username"
                 class="username-input"
             />
           </div>

          <!-- Button Container for Save and Delete -->
          <div class="button-container">
            <Button variant="destructive">

              Delete
            </Button>
            <button type="button" class="primary-button">Save</button>
          </div>
        </div>

        <!-- Email and Name Container -->
        <div class="box-container email-name-container">
           <h1>Profile Information</h1>
           <h4>Update your account's profile name and email address.</h4>
          <div class="form-group">
            <Label for="name">Name:</Label>
            <Input
              type="text"
              id="name"
              v-model="user.name"
            />
          </div>

          <div class="form-group">
            <Label for="email">Email:</Label>
            <Input
              type="email"
              id="email"
              v-model="user.email"

            />
          </div>
          <button type="button" class="primary-button">Save</button>
        </div>
      </div>

      <!-- Password Change Container -->
      <div class="box-container password-change-container">
        <h1>Change Password</h1>
        <h4>Keep your account safe by choosing a strong, random password.</h4>
        <div class="form-group">
          <Label for="oldpass">Current Password:</Label>
          <Input
            type="password"
            id="oldpass"
            v-model="oldPassword"

          />
        </div>

        <div class="form-group">
          <Label for="newpass">New Password:</Label>
          <Input
            type="password"
            id="newpass"
            v-model="newPassword"
          />
        </div>

        <div class="form-group">
          <Label for="conpass">Confirm Password:</Label>
          <Input
            type="password"
            id="conpass"
            v-model="confirmPassword"
          />
        </div>
        <Button type="button" class="primary-button">Save</Button>
      </div>

      <!-- Delete Account Container -->
      <div class="delete-account-container">
        <Label>Delete Account</Label>
        <p class="delete-description">
          If you want to delete your account, click the button below. Note that this action cannot be undone.
        </p>
        <Button type="button" @click="deleteAccount" class="secondary-button">Delete Account</Button>
      </div>
    </form>
  </div>
</template>

<script>

import {Button } from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {Label} from "@/components/ui/label";

export default {
  data() {
    return {
      user: {
        name: '',
        email: '',
        profilePicture: null,
      },
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
    };
  },
  components:{
    Button,
    Input,
    Label,
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.user.profilePicture = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    triggerFileInput() {
      document.getElementById('profile-picture').click();
    },
    deleteProfilePicture() {
      if (confirm('Are you sure you want to delete your profile picture?')) {
        this.user.profilePicture = null;
      }
    },
    async handleSubmit() {
      if (this.newPassword && this.newPassword !== this.confirmPassword) {
        alert("New passwords do not match!");
        return;
      }

      alert('Profile updated (simulated)!');
      console.log('Updated user data:', this.user);

      this.oldPassword = '';
      this.newPassword = '';
      this.confirmPassword = '';
    },
    deleteAccount() {
      if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
        alert('Account deleted (simulated)!');
        console.log('User account deleted');
        this.user = {};
      }
    },
  },
};
</script>

<style scoped>
.user-profile {
  max-width: 1200px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.aligned-container {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.box-container {
  padding: 20px;
  border-radius: 10px;
  border: 1px;
  border-style: solid;
  width: 100%;
}

.profile-container {
  flex: 1;
  text-align: center;
}

.email-name-container {
  flex: 2;
}

.password-change-container,
.delete-account-container {
  margin-top: 20px;
}

.profile-picture-container {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  cursor: pointer;
}

.profile-picture {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.person-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 5px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #f0f0f0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  margin-top: 15px;
  margin-bottom: 5px;
  display: block;
}

input {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 7px;
  width: 80%;
  font-size: 14px;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #101010;
  outline: none;
}

.primary-button,
.secondary-button {
  padding: 6px 25px;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: block;
  margin-top: 10px;
}

.primary-button {
  background-color: #101010;
  color: white;
  border: none;
}

.primary-button:hover {
  background-color: #202020;
}

.secondary-button {
  padding: 6px 20px;
  background-color: #e74c3c;
  color: white;
  border: none;
}

.secondary-button:hover {
  background-color: #c0392b;
}

.delete-account-container {
  margin-top: 20px;
  padding: 20px;
  border-radius: 10px;
  background-color: #fff3f3;
  border: 1px solid #e74c3c;
}

.delete-description {
  margin-bottom: 10px;
  font-size: 16px;
  color: #e74c3c;
}

h1{
  font-weight: bold;
  font-size: 24px;
}

h4{
  font-size: 16px;
  color: lightslategrey;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.username-display {
  margin-top: 10px;
  font-size: 16px;
  color: #101010;
}

.username-input {
  border: none;
  outline: none;
  border-bottom: 1px solid #ccc;
  font-size: 16px;
  color: #101010;
  width: auto;
}

.username-input::placeholder {
  color: #aaa;
}

</style>
