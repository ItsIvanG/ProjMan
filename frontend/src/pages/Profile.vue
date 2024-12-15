<template>
  <div class="user-profile px-[100px]">
    <form @submit.prevent="handleSubmit">
      <!-- Aligned Containers: Profile and Email/Name -->
      <div class="grid-cols-3 grid gap-4 mb-5">
        <!-- Profile Container -->
        <Card class="col-span-1">
          <CardHeader>
             <CardTitle>Profile Picture</CardTitle>
          <CardDescription>Set a new profile picture for your account.</CardDescription>

          </CardHeader>
          <CardContent>
            <div class="flex justify-center">
               <div class="profile-picture-container w-[100px] h-[100px] " @click="triggerFileInput" >
            <img
              v-if="user.profile_picture"
              :src="profilePictureUrl"
              alt="Profile Preview"
              class="profile-picture"
            />
            <span v-else class="person-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#101010" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4z"/><path d="M20 20c0-4.42-3.58-8-8-8s-8 3.58-8 8"/></svg>
            </span>
            <input type="file" id="profile-picture" @change="handleFileChange" hidden />
          </div>

            </div>


          </CardContent>
          <CardFooter>
             <Button variant="destructive">Delete</Button>
            <Button  @click="uploadProfilePicture" class="ml-3">Save</Button>
          </CardFooter>

        </Card>

        <!-- Email and Name Container -->
        <Card class="col-span-2">
          <CardHeader>
             <CardTitle>Profile Information</CardTitle>
           <CardDescription>Update your account's profile name, username and email address.</CardDescription>

          </CardHeader>
          <CardContent>
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
                        <Label for="email">Username:</Label>

              <Input
                 type="text"
                 v-model="user.username"
                 placeholder="@username"
                 class="username-input"
             />
          </CardContent>

          <CardFooter>
                      <Button >Save</Button>
          </CardFooter>
        </Card>
      </div>

      <!-- Password Change Container -->
      <Card class="mb-5" >
        <CardHeader>
           <CardTitle>Change Password</CardTitle>
        <CardDescription>Keep your account safe by choosing a strong, random password.</CardDescription>

        </CardHeader>
        <CardContent>
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
        </CardContent>
       <CardFooter>
                 <Button type="button" class="primary-button" @click="handleSubmitPass">Save</Button>
       </CardFooter>
      </Card>

      <!-- Delete Account Container -->
      <Card class="border border-destructive">
        <CardHeader>
            <CardTitle>Delete Account</CardTitle>
            <CardDescription>
              If you want to delete your account, click the button below. Note that this action cannot be undone.
            </CardDescription>
        </CardHeader>
        <CardFooter>
          <Button type="button" @click="deleteAccount" variant="destructive">Delete Account</Button>
        </CardFooter>
      </Card>

    </form>
  </div>
</template>

<script setup lang="ts">
import {computed, ref, onMounted} from "vue";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardTitle,
  CardContent,
  CardHeader,
  CardFooter,
  CardDescription,
} from "@/components/ui/card";
import {useAuthStore} from "@/store/auth.ts";
import {getAPI} from "@/axios.ts";

interface User {
  name?: string;
  email?: string;
  username?: string;
  role?: string;
  profile_picture?: string | null;
  password?: string;
}


// Reactive state
const user = ref<User>({
  name: "",
  email: "",
  profile_picture: "",
});

const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");



// Methods


const updateUserNameAndEmail = async (userId: number, data: UpdateUserData): Promise<void> => {
  try {
    console.log("trying to update usern: ",user.value.name);
     if (!user.value.name || !user.value.email) {
    alert("Name and email fields are required!");
    return;
  }

    await getAPI.put(`api/userprofile/${userId}/`, data);
  } catch (error) {
    console.error("Error updating name and email:", error);
    throw error;
  }
};

const updateUserPassword = async (userId: number, data: UpdatePasswordData): Promise<void> => {
  try {
    await getAPI.put(`api/updatepass/${userId}/`, data);
  } catch (error) {
    console.error("Error updating password:", error);
    throw error;
  }
};

const profilePicture = ref<File | null>(null);

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (file) {
    const reader = new FileReader();
    profilePicture.value = file;
    reader.onload = (e: ProgressEvent<FileReader>) => {
      user.value.profilePicture = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

const triggerFileInput = () => {
  const fileInput = document.getElementById("profile-picture") as HTMLInputElement;
  if (fileInput) {
    fileInput.click();
  }
};

const deleteProfilePicture = () => {
  if (confirm("Are you sure you want to delete your profile picture?")) {
    user.value.profilePicture = null;
  }
};

const handleSubmit = async () => {

  await updateUserNameAndEmail(userId.value,{name: user.value.name, email: user.value.email, username: user.value.username});
  alert("User details updated!");
};

const handleSubmitPass = async () => {
  if (newPassword.value && newPassword.value !== confirmPassword.value) {
    alert("New passwords do not match!");
    return;

  }
 if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    alert("All fields are required!");
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    alert("New password and confirmation do not match!");
    return;
  }

  try {
    await updateUserPassword(userId.value, {
      oldPassword: oldPassword.value,
      newPassword: newPassword.value,
    });
    alert("Password updated successfully!");
    oldPassword.value = "";
    newPassword.value = "";
    confirmPassword.value = "";
  } catch (error) {
    alert("Failed to update password. Please ensure your old password is correct.");
    console.error(error);
  }
};


const deleteAccount = () => {
  if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
    alert("Account deleted (simulated)!");
    console.log("User account deleted");
    user.value = { name: "", email: "", profilePicture: null };
  }
};
const authStore = useAuthStore();

const userId = computed(() => authStore.user?.id);

const getUserById = async (userId: number): Promise<User> => {
  try {
    console.log("trying to fetch profile by ID: ",userId);
    const response = await getAPI.get(`/api/userprofile/${userId}/`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching user:", error);
    throw error;
  }
};

const uploadProfilePicture = async () => {
  if (!profilePicture.value) {
    alert("Please select a profile picture to upload.");
    return;
  }

  const formData = new FormData();
  formData.append("profile_picture", profilePicture.value);

  try {
    const response = getAPI.post(
      `api/uploadpicture/${userId.value}/`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    alert("Profile picture uploaded successfully!");
    console.log("Uploaded profile picture:", response.data);
  } catch (error) {
    console.error("Error uploading profile picture:", error);
    alert("Failed to upload profile picture.");
  }
};

const profilePictureUrl = computed(() =>
  user.value.profile_picture ? `http://localhost:8000/${user.value.profile_picture}` : null
);

onMounted(async () => {
  try {
    user.value = await getUserById(userId.value);
  } catch (error) {
    console.error("Failed to load user:", error);
  }
});

</script>


<style scoped>

.profile-picture {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

</style>