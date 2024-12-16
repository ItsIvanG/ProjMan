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
             <Avatar class="h-[100px] w-[100px]">
                <AvatarImage :src="profilePictureUrl" alt="@shadcn" />
                <AvatarFallback><SquareUser/></AvatarFallback>
              </Avatar>
                   <div class=" mt-5 " >
                    <Input id="picture"  @change="handleFileChange" type="file" class="file-input file:text-muted-foreground" />
                  </div>

          </CardContent>
          <CardFooter>
             <Button  @click="deleteProfilePicture" variant="destructive">Delete</Button>
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
          <Button type="button" @click="showDeleteDialog" variant="destructive">Delete Account</Button>
        </CardFooter>
      </Card>

    </form>
  </div>

  <Dialog v-model:open="isDeleteDialog" @close="closeDialog">
      <!-- Updated DialogContent size -->
      <DialogContent class="max-w-[600px]">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Delete Account?</DialogTitle>
          <DialogDescription class=" text-lg">
          Are you sure you want to delete your account? If you are a project manager, This will permanently delete all associated projects and its members. This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        <DialogFooter>
          <Button type="button" @click="closeDialog" class="w-full sm:w-auto" variant="outline">
            Cancel
          </Button>
          <Button type="button" @click="deleteUser" class="w-full sm:w-auto" variant="destructive">
            <Trash class="mr-2 h-4 w-4" />
            Delete
          </Button>

        </DialogFooter>
      </DialogContent>
    </Dialog>
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
import {getAPI} from "@/axios";

import { useToast } from '@/components/ui/toast/use-toast'
import {Avatar, AvatarFallback, AvatarImage} from "@/components/ui/avatar";
import {Trash, SquareUser} from "lucide-vue-next";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import router from "@/router.ts";
const { toast } = useToast()

// interface User {
//   name?: string;
//   email?: string;
//   username?: string;
//   role?: string;
//   profile_picture?: string | null;
//   password?: string;
// }


// Reactive state
const user = ref({
});

const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");



// Methods


const updateUserNameAndEmail = async (userId: number, data: UpdateUserData): Promise<void> => {
  try {

    console.log("trying to update usern: ",user.value.name);
     if (!user.value.name || !user.value.email) {
    toast({title: "Name and email fields are required!",variant:"destructive"});
    return;
  }

    await getAPI.put(`api/userprofile/${userId}/`, data);
           toast({
        title: 'Profile details updated!',
      });
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





const handleSubmit = async () => {

  await updateUserNameAndEmail(userId.value,{name: user.value.name, email: user.value.email, username: user.value.username});

  // alert("User details updated!");
};

const handleSubmitPass = async () => {
  if (newPassword.value && newPassword.value !== confirmPassword.value) {
    toast({
        title: 'Passwords do not match!',
      variant: "destructive"
      });
    return;

  }
 if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
      toast({
        title: 'All password fields required!',
      variant: "destructive"
      });
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    toast({
        title: 'Passwords do not match!',
      variant: "destructive"
      });
    return;
  }

  try {
    await updateUserPassword(userId.value, {
      oldPassword: oldPassword.value,
      newPassword: newPassword.value,
    });
    toast({
        title: 'Password updated!',
      });
    oldPassword.value = "";
    newPassword.value = "";
    confirmPassword.value = "";
  } catch (error) {
    toast({
        title: 'Incorrect old password!',
      variant: "destructive"
      });
    console.error(error);
  }
};

const authStore = useAuthStore();



const userId = computed(() => authStore.user?.id);

const getUserById = async (userId: number) => {
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
  // if (!profilePicture.value) {
  //   alert("Please select a profile picture to upload.");
  //   return;
  // }

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
    // alert("Profile picture uploaded successfully!");
    toast({
        title: 'Profile picture uploaded successfully!',
      });
    window.location.reload();
    console.log("Uploaded profile picture:", response.data);
  } catch (error) {
    console.error("Error uploading profile picture:", error);
    alert("Failed to upload profile picture.");
  }
};
const deleteProfilePicture = () => {
      try {
      const response =  getAPI.delete(`api/deletepicture/${userId.value}/`);
      window.location.reload();
      console.log(response.data.detail); // Success message
    } catch (error: any) {
      console.error(error.response?.data?.detail || "An error occurred.");

  }
};
const profilePictureUrl = computed(() =>
  user.value.profile_picture ? `http://localhost:8000/${user.value.profile_picture}` : null
);

const deleteUser = async () => {
  try {
    const response = getAPI.delete(`user/${userId.value}/delete/`);
    console.log(response.data.detail); // Success message
    router.push('/login');
  } catch (error: any) {
    console.error(error.response?.data?.detail || "An error occurred.");
     router.push('/login');
  }
};

const isDeleteDialog = ref(false);

const closeDialog = () => {
  isDeleteDialog.value = false;
};

const showDeleteDialog = () =>{
  isDeleteDialog.value = true;
}

onMounted(async () => {
  try {
    user.value = await getUserById(userId.value);
  } catch (error) {
    console.error("Failed to load user:", error);
  }
});

</script>


<style scoped>

.file-input {
   color: var(--primary);

}

</style>