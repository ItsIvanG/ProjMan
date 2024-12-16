<template xmlns="http://www.w3.org/1999/html">

  <div class="grid lg:grid-cols-2">
    <div class="bg-secondary min-h-full  flex flex-col">
    <sidecolumn_welcome/>
    </div>
    <div class="p-[100px] h-screen flex items-center  ">
      <div class=" w-full border p-6 rounded-lg  shadow-md  ">
    <!-- Title and Theme Toggle -->
      <div class="flex flex-col  items-center  mb-8">
        <h3 class="text-3xl font-bold text-center">Create an account</h3>
      </div>

<!--    <div class="flex justify-between items-right mb-4">-->
<!--      <div-->
<!--        v-for="(step, index) in steps"-->
<!--        :key="index"-->
<!--        class="flex flex-col items-center space-x-2"-->
<!--      >-->
<!--        &lt;!&ndash; Step number &ndash;&gt;-->
<!--        <div-->
<!--          :class="{-->
<!--            'bg-gray-500 text-white': currentStep !== index + 1,-->
<!--            'bg-gray-300 text-gray-700': currentStep === index + 1 && !isDarkMode,-->
<!--            'bg-gray-700 text-gray-300': currentStep === index + 1 && isDarkMode,-->
<!--          }"-->
<!--          class="w-8 h-8 flex items-center justify-center rounded-full font-bold"-->
<!--        >-->
<!--          {{ index + 1 }}-->
<!--        </div>-->
<!--        &lt;!&ndash; Step Title &ndash;&gt;-->
<!--        <div-->
<!--          :class="{-->
<!--            'text-gray-300': currentStep !== index + 1,-->
<!--            'text-gray-300': currentStep === index + 1 && !isDarkMode,-->
<!--            'text-gray-500': currentStep === index + 1 && isDarkMode,-->
<!--          }"-->
<!--          class="text-sm font-semibold"-->
<!--        >-->
<!--          {{ step }}-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->

      <!-- Form Content -->
<div v-if="currentStep === 1" class="grid grid-cols-1">

<!-- Input Form with Consistent Spacing -->
<div class="space-y-2">
  <!-- First Name and Last Name Inputs Side by Side -->
    <!-- First Name Input -->

      <div class="relative">
        <div class="flex items-center justify-between mb-2 ">
          <label for="firstname" class="block font-bold">Name</label>
          <div v-if="showErrors.firstName" class="text-red-500 text-sm">This field is required</div>
        </div>
        <div class="relative">
          <Input
            v-model="formData.firstName"
            id="firstname"
            type="text"
            placeholder="Enter Name"
            class="border rounded-md w-full h-10 px-2 f"
            required
          />
          <span class="absolute right-3 top-1/2 transform -translate-y-1/2">
            <AkPerson class="cursor-pointer" />
          </span>
        </div>


    <!-- Last Name Input -->
    <div class="w-1/2">
      <div class="relative">
<!--        <div class="flex items-center justify-between mb-2">-->
<!--          <label for="lastname" class="block font-bold">Last Name</label>-->
<!--          <div v-if="showErrors.lastName" class="text-red-500 text-sm">This field is required</div>-->
<!--        </div>-->
<!--        <div class="relative">-->
<!--          <input-->
<!--            v-model="formData.lastName"-->
<!--            id="lastname"-->
<!--            type="text"-->
<!--            placeholder="Enter Last Name"-->
<!--            class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"-->
<!--            required-->
<!--          />-->
<!--          <span class="absolute right-3 top-1/2 transform -translate-y-1/2">-->
<!--            <AkPerson class="cursor-pointer" />-->
<!--          </span>-->
<!--        </div>-->
      </div>
    </div>
  </div>

  <!-- Email Input -->
  <div class="relative">
    <div class="flex items-center justify-between mb-2">
      <label for="email" class="block font-bold">Email</label>
      <div v-if="showErrors.email" class="text-red-500 text-sm">This field is required</div>
    </div>
    <div class="relative">
      <Input
        v-model="formData.email"
        id="email"
        type="email"
        placeholder="example@mail.com"
        class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"
        required
      />
      <span class="absolute right-3 top-1/2 transform -translate-y-1/2">
        <IoOutlineMail class="cursor-pointer" />
      </span>
    </div>
  </div>


  <!-- Username Input -->
  <div class="relative">
    <div class="flex items-center justify-between mb-2">
      <label for="username" class="block font-bold">Username</label>
      <div v-if="showErrors.username" class="text-red-500 text-sm">This field is required</div>
    </div>
    <div class="relative">
      <Input
        v-model="formData.username"
        id="username"
        type="text"
        placeholder="Your username"
        class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"
        required
      />
      <span class="absolute right-3 top-1/2 transform -translate-y-1/2">
        <AkPerson class="cursor-pointer" />
      </span>
    </div>
  </div>

  <!-- Password Input -->
  <div class="relative">
    <div class="flex items-center justify-between mb-2">
      <label for="password" class="block font-bold">Password</label>
      <span v-if="showErrors.password" class="text-red-500 text-sm">This field is required</span>
    </div>
    <div class="relative">
      <Input
        v-model="formData.password"
        id="password"
        :type="showPassword ? 'text' : 'password'"
        placeholder="Enter Password"
        class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"
        required
      />
      <span
        class="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer"
        @click="togglePassword('password')"
      >
        <AkEyeClosed v-if="!showPassword" />
        <AkEyeOpen v-if="showPassword" />
      </span>
    </div>
    <div v-if="passwordInvalid" class="text-red-500 text-sm">
      Password must be more than 8 characters, one uppercase letter, and one number.
    </div>
  </div>

  <!-- Confirm Password Input -->
  <div class="relative">
    <div class="flex items-center justify-between mb-2">
      <label for="confirmPassword" class="block font-bold">Confirm Password</label>
      <div v-if="showErrors.confirmPassword" class="text-red-500 text-sm">This field is required</div>
    </div>
    <div class="relative">
      <Input
        v-model="formData.confirmPassword"
        id="confirmPassword"
        :type="showConfirmPassword ? 'text' : 'password'"
        placeholder="Re-type Password"
        class="border rounded-md w-full h-10 px-2"
        required
      />
      <span
        class="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer"
        @click="togglePassword('confirmPassword')"
      >
        <AkEyeClosed v-if="!showConfirmPassword" />
        <AkEyeOpen v-if="showConfirmPassword" />
      </span>
    </div>
    <div v-if="passwordMismatch" class="text-red-500 text-sm">Passwords do not match</div>
  </div>

  <!-- Birthday Input -->
<!--  <div class="relative">-->
<!--    <div class="flex items-center justify-between mb-2">-->
<!--      <label for="birthday" class="block font-bold">Birthday</label>-->
<!--      <div v-if="showErrors.birthday" class="text-red-500 text-sm">This field is required</div>-->
<!--    </div>-->
<!--    <div class="relative">-->
<!--      <Input-->
<!--        v-model="formData.birthday"-->
<!--        id="birthday"-->
<!--        type="date"-->
<!--        class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"-->
<!--        required-->
<!--        ref="birthdayInput"-->
<!--      />-->
<!--      <span-->
<!--        class="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer"-->
<!--        @click="toggleDatePicker"-->
<!--      >-->
<!--        <CiCalendarDate/>-->
<!--      </span>-->
<!--    </div>-->
<!--  </div>-->

          <!-- Gender Input -->
<!--          <div class="relative">-->
<!--            <div class="flex items-center justify-between mb-2">-->
<!--              <label for="gender" class="block font-bold">Gender</label>-->
<!--              <div v-if="showErrors.gender" class="text-red-500 text-sm">This field is required</div>-->
<!--            </div>-->
<!--            <select-->
<!--              v-model="formData.gender"-->
<!--              id="gender"-->
<!--              :class="darkMode ? 'w-full border border-white rounded p-2 bg-black text-white' : 'w-full border border-black rounded p-2 bg-white text-black'"-->
<!--              required-->
<!--            >-->
<!--              <option value="">Select</option>-->
<!--              <option value="Male">Male</option>-->
<!--              <option value="Female">Female</option>-->
<!--              <option value="Other">Other</option>-->
<!--            </select>-->
<!--          </div>-->
        </div>
      </div>


<div v-if="currentStep === 2" class="space-y-4">
  <!-- Terms and Conditions Label -->
  <label
    class="block mb-1 font-bold"
  >
    Terms and Conditions
  </label>

  <!-- Terms and Conditions Text Area -->
  <ScrollArea class="h-[300px] w-flex rounded-md border p-4">
Welcome to ProjMan!
<br><br>
These terms and conditions ("Terms") govern your access to and use of the ProjMan website and services ("Services"). By using our website, you agree to comply with and be bound by these Terms. If you do not agree with these Terms, please do not use the Services.<br>
1. Acceptance of Terms<br>
By accessing or using the ProjMan platform, you agree to comply with these Terms, as well as our Privacy Policy. We reserve the right to modify, update, or change these Terms at any time. Any changes will be posted on this page, and the updated Terms will be effective immediately upon posting.<br><br>

2. Use of the Service<br>
ProjMan provides a platform for project management tools, including task management, time tracking, and collaboration features. You agree to:<br>
- Use the Service only for lawful purposes and in accordance with these Terms.<br>
- Not misuse or interfere with the Service in any way.<br>
- Not attempt to gain unauthorized access to the Service, servers, or networks.<br><br>

3. Account Registration<br>
To use certain features of ProjMan, you must create an account. You are responsible for maintaining the confidentiality of your account credentials, and you agree to notify us immediately of any unauthorized use of your account. You must be at least 18 years old to register for an account.<br><br>

4. Subscription Plans and Payment<br>
ProjMan offers both free and paid subscription plans. If you subscribe to a paid plan, you agree to pay the applicable subscription fees in accordance with the plan you choose. Payments are non-refundable, and fees are subject to change. You will be notified of any changes to the fees.<br><br>

5. License to Use the Service<br>
ProjMan grants you a limited, non-exclusive, non-transferable, revocable license to access and use the Service for your internal business or personal use. You may not distribute, modify, or create derivative works based on the Service.<br><br>

6. User Content<br>
You are solely responsible for the content you upload, create, or share through the Service ("User Content"). By uploading or submitting content to ProjMan, you grant us a worldwide, royalty-free, and non-exclusive license to use, display, and distribute the content within the Service.<br><br>

7. Privacy<br>
Your use of the Service is also governed by our Privacy Policy, which outlines how we collect, use, and protect your personal data. Please review our Privacy Policy to understand how your information is handled.<br><br>

8. Prohibited Activities<br>
You agree not to:<br>
- Violate any applicable laws, regulations, or third-party rights.<br>
- Engage in any activity that could harm the Service or other users.<br>
- Use the Service for any illegal or unauthorized purpose, including but not limited to spamming, hacking, or distributing malware.<br>
- Attempt to reverse-engineer, decompile, or disassemble the Service.<br><br>

9. Termination<br>
We reserve the right to suspend or terminate your access to the Service if you violate these Terms or engage in any unlawful activities. You may also terminate your account at any time by contacting us.<br><br>

10. Disclaimer of Warranties<br>
The Service is provided "as is" without any warranties of any kind, either express or implied. We do not guarantee that the Service will be uninterrupted or error-free. You use the Service at your own risk.<br><br>

11. Limitation of Liability<br>
In no event shall ProjMan or its affiliates be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or in connection with your use of the Service.<br><br>

12. Indemnification<br>
You agree to indemnify and hold harmless ProjMan, its affiliates, employees, and partners from any claims, damages, losses, liabilities, or expenses arising from your use of the Service or violation of these Terms.<br><br>

13. Governing Law<br>
These Terms shall be governed by and construed in accordance with the laws of your jurisdiction, without regard to its conflict of law principles. Any disputes arising from these Terms shall be resolved in the courts of [Your jurisdiction].<br><br>

14. Changes to the Terms<br>
We may update these Terms at any time. You will be notified of any material changes, and your continued use of the Service after such changes will constitute your acceptance of the new Terms.<br><br>
</ScrollArea>

  <!-- Terms Agreement Checkbox -->
  <div v-if="showErrors.agreeTerms" class="text-red-500 text-sm">This field is required</div>

  <div>
    <label class="inline-flex items-center">
      <input
        type="checkbox"
        v-model="formData.agreeTerms"
        class="mr-2"
        required
      />
      <span>
        I agree to the terms and conditions.
      </span>
    </label>
  </div>
</div>

<div v-if="currentStep === 3" class="space-y-4">
  <!-- Profile Picture Upload -->
  <div>
    <label for="profilePicture" class="block mb-1 font-bold">
      Profile Picture
    </label>
    <input
      id="profilePicture"
      type="file"
      @change="handleFileUpload"
      accept="image/*"
      class="w-full border rounded p-2"
      required
    />
  </div>

  <!-- Profile Picture Preview -->
  <div v-if="formData.profilePicture" class="relative mt-4">
    <div class="flex justify-center">
      <img
        :src="formData.profilePicture"
        alt="Profile Picture Preview"
        class="w-48 h-48 object-cover rounded-full cursor-pointer transition-transform duration-300 hover:scale-110 border-2"
      />
    </div>
  </div>
</div>

<!-- Navigation Buttons -->
<div class="flex justify-between mt-5">
  <Button
    v-if="currentStep > 1"
    @click="prevStep"
    class="px-4 py-2 border rounded"
  >
    Back
  </Button>
  <Button variant="outline" v-else @click="router.push('/login')">Back to Log in</Button>
<p></p>
  <Button
    v-if="currentStep < 2"
    @click="nextStep"
    class="px-4 py-2 border rounded  "
    :disabled="isNextDisabled"
    variant="default"
  >
    Next
  </Button>

  <Button
    v-if="currentStep === 2"
    @click="register"
    class="px-4 py-2 border rounded"
  >
    Register
  </Button>
</div>
    </div>
        </div>
    </div>

</template>
<script setup lang="ts">
import { ref, reactive, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { AkEyeClosed, AkEyeOpen, IoOutlineMail, AkPerson, CiCalendarDate } from "@kalimahapps/vue-icons";
import { Input  } from "@/components/ui/input";
import { Textarea  } from "@/components/ui/textarea";
import { ScrollArea  } from "@/components/ui/scroll-area";
import { Button  } from "@/components/ui/button";

import {toast} from "@/components/ui/toast";
import Sidecolumn_welcome from "@/components/reusable/sidecolumn_welcome.vue";
import { getCSRFToken } from "@/store/auth";

// Props
defineProps({
  text: {
    type: String,
    required: true,
  },
  maxLength: {
    type: Number,
    default: 100,
  },
});

// Router
const router = useRouter();

// Data
const currentStep = ref(1);
const steps = ["Account Setup", "Terms and Conditions", "Upload Image"];
const formData = reactive({
  firstName: "",
  email: "",
  username: "",
  password: "",
  confirmPassword: "",
  birthday: "",
  gender: "",
  agreeTerms: false,
  profilePicture: null as string | null,
  isExpanded: false,
});
const showErrors = reactive({
  firstName: false,
  email: false,
  username: false,
  password: false,
  confirmPassword: false,
  birthday: false,
  gender: false,
  agreeTerms: false,
  profilePicture: false,
});
const passwordInvalid = ref(false);
const passwordMismatch = ref(false);
const isFieldTouched = reactive({
  firstName: false,
  email: false,
  username: false,
  password: false,
  confirmPassword: false,
  birthday: false,
  gender: false,
  agreeTerms: false,
});
const showDatePicker = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isDarkMode = ref(false);

// Computed
const isTruncatable = computed(() => text.length > maxLength);
const truncatedText = computed(() =>
  isTruncatable.value ? text.slice(0, maxLength) + "..." : text
);
const fullText = computed(() => text);

// Watchers
watch(
  () => formData.firstName,
  (value) => {
    if (isFieldTouched.firstName) {
      showErrors.firstName = !value || value.trim().length === 0;
    }
  }
);
watch(
  () => formData.email,
  (value) => {
    if (isFieldTouched.email) {
      showErrors.email = !value;
    }
  }
);
watch(
  () => formData.password,
  (value) => {
    if (isFieldTouched.password) {
      showErrors.password = !value;
      passwordInvalid.value = !validatePassword(value);
    }
  }
);
watch(
  () => formData.confirmPassword,
  (value) => {
    if (isFieldTouched.confirmPassword) {
      showErrors.confirmPassword = !value;
      passwordMismatch.value = value !== formData.password;
    }
  }
);

// Methods
const validatePassword = (password: string) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
  return regex.test(password);
};

const validateField = (field: keyof typeof formData) => {
  isFieldTouched[field] = true;
  if (!formData[field]) {
    showErrors[field] = true;
  } else {
    showErrors[field] = false;
    if (field === "password") {
      passwordInvalid.value = !validatePassword(formData.password);
    }
    if (field === "confirmPassword") {
      passwordMismatch.value = formData.password !== formData.confirmPassword;
    }
  }
};

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      formData.profilePicture = e.target?.result as string;
      showErrors.profilePicture = false;
      profilePicture.value = file;
    };
    reader.readAsDataURL(file);
  } else {
    showErrors.profilePicture = true;
  }
};

const nextStep = () => {
  let valid = true;
  if (currentStep.value === 1) {
    ["firstName", "email", "username", "password", "confirmPassword"].forEach((field) => {
      validateField(field as keyof typeof formData);
      if (
        showErrors[field as keyof typeof formData] ||
        passwordInvalid.value ||
        passwordMismatch.value
      ) {
        valid = false;
      }
    });
  } else if (currentStep.value === 2) {
    validateField("agreeTerms");
    if (showErrors.agreeTerms) valid = false;
    return;
  }
  if (valid) currentStep.value++;
};

const prevStep = () => {
  currentStep.value--;
};



const profilePicture = ref<File | null>(null);

const handleError = (error: any) => {
  try {
    // Parse the error response if it's a stringified JSON
    const parsedError = JSON.parse(error.error);

    // Get the first error message for 'email' or 'username'
    const emailError = parsedError.email ? parsedError.email[0].message : null;
    const usernameError = parsedError.username ? parsedError.username[0].message : null;

    // Choose which error to show. In this case, I'll prioritize email over username.
    const errorMessage = emailError || usernameError || 'Unknown error occurred';

    // Display error toast
    toast({
      title: 'Error',
      description: errorMessage,
    });
  } catch (err) {
    // Fallback in case the error is not in the expected format
    console.error('Error parsing error message:', err);
    toast({
      title: 'Error',
      description: 'An unknown error occurred.',
    });
  }
};
const register = async () => {
  let valid = true;
      validateField("agreeTerms");
    if (showErrors.agreeTerms) return;
  try {
    console.log("trying to upload formdataPicture: ", formData.profilePicture);
    const response = await fetch("http://localhost:8000/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({
        name: formData.firstName,
        email: formData.email,
        username: formData.username,
        password: formData.password,
      }),
      credentials: "include",
    });

    if (!response.ok) {
      const errorMessage = await response.text();
               console.log(errorMessage);
      toast({
      variant:"destructive",
      title:"An error occurred during registration: Email invalid or username already exists."
    });

      return;
    }

    const data = await response.json();
    if (data.success) {
       toast({title: "Registration successful! Redirecting to login..."});
      router.push("/login");
    } else {
      toast({title: "Registration failed: " + (data.error || "Unknown error")});
    }
  } catch (err) {
    console.log(err);
    toast({title: "An error occurred during registration: " + (err as Error).message});
  }
};

const togglePassword = (field: "showPassword" | "showConfirmPassword") => {
  if (field === "showPassword") {
    showPassword.value = !showPassword.value;
  } else if (field === "showConfirmPassword") {
    showConfirmPassword.value = !showConfirmPassword.value;
  }
};

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
};

const toggleDatePicker = () => {
  const input = document.querySelector<HTMLInputElement>("#birthdayInput");
  input?.showPicker();
};


</script>
