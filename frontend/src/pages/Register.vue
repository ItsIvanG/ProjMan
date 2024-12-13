<template xmlns="http://www.w3.org/1999/html">
  <div :class="[isDarkMode ? 'dark' : 'light', 'flex items-center justify-end min-h-screen']">
    <div class="w-1/2 flex items-center justify-center">
    </div>

  <div class="max-w-[600px] w-full h-[820px] border p-6 rounded-lg shadow-md overflow-auto mr-20">
    <!-- Title and Theme Toggle -->
      <div class="flex flex-col justify-center items-center mb-8">
        <h3 class="text-3xl font-bold text-center">Register Your Account</h3>
      </div>

    <div class="flex justify-between items-right mb-4">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="flex flex-col items-center space-x-2"
      >
        <!-- Step number -->
        <div
          :class="{
            'bg-gray-500 text-white': currentStep !== index + 1,
            'bg-gray-300 text-gray-700': currentStep === index + 1 && !isDarkMode,
            'bg-gray-700 text-gray-300': currentStep === index + 1 && isDarkMode,
          }"
          class="w-8 h-8 flex items-center justify-center rounded-full font-bold"
        >
          {{ index + 1 }}
        </div>
        <!-- Step Title -->
        <div
          :class="{
            'text-gray-300': currentStep !== index + 1,
            'text-gray-300': currentStep === index + 1 && !isDarkMode,
            'text-gray-900': currentStep === index + 1 && isDarkMode,
          }"
          class="text-sm font-semibold"
        >
          {{ step }}
          </div>
        </div>
      </div>

      <!-- Form Content -->
<div v-if="currentStep === 1" class="grid grid-cols-1">

<!-- Input Form with Consistent Spacing -->
<div class="space-y-2">
  <!-- First Name and Last Name Inputs Side by Side -->
  <div class="flex justify-between gap-6">
    <!-- First Name Input -->
    <div class="w-1/2">
      <div class="relative">
        <div class="flex items-center justify-between mb-2">
          <label for="firstname" class="block font-bold">First Name</label>
          <div v-if="showErrors.firstName" class="text-red-500 text-sm">This field is required</div>
        </div>
        <div class="relative">
          <input
            v-model="formData.firstName"
            id="firstname"
            type="text"
            placeholder="Enter First Name"
            class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"
            required
          />
          <span class="absolute right-3 top-1/2 transform -translate-y-1/2">
            <AkPerson class="cursor-pointer" />
          </span>
        </div>
      </div>
    </div>

    <!-- Last Name Input -->
    <div class="w-1/2">
      <div class="relative">
        <div class="flex items-center justify-between mb-2">
          <label for="lastname" class="block font-bold">Last Name</label>
          <div v-if="showErrors.lastName" class="text-red-500 text-sm">This field is required</div>
        </div>
        <div class="relative">
          <input
            v-model="formData.lastName"
            id="lastname"
            type="text"
            placeholder="Enter Last Name"
            class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"
            required
          />
          <span class="absolute right-3 top-1/2 transform -translate-y-1/2">
            <AkPerson class="cursor-pointer" />
          </span>
        </div>
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
      <input
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
      <input
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
      <input
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
      Password must be more than 8 characters, with at least one special character, one uppercase letter, and one number.
    </div>
  </div>

  <!-- Confirm Password Input -->
  <div class="relative">
    <div class="flex items-center justify-between mb-2">
      <label for="confirmPassword" class="block font-bold">Confirm Password</label>
      <div v-if="showErrors.confirmPassword" class="text-red-500 text-sm">This field is required</div>
    </div>
    <div class="relative">
      <input
        v-model="formData.confirmPassword"
        id="confirmPassword"
        :type="showConfirmPassword ? 'text' : 'password'"
        placeholder="Re-type Password"
        class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"
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
  <div class="relative">
    <div class="flex items-center justify-between mb-2">
      <label for="birthday" class="block font-bold">Birthday</label>
      <div v-if="showErrors.birthday" class="text-red-500 text-sm">This field is required</div>
    </div>
    <div class="relative">
      <input
        v-model="formData.birthday"
        id="birthday"
        type="date"
        class="border rounded-md w-full h-10 px-2 focus:outline-none focus:ring-2"
        required
        ref="birthdayInput"
      />
      <span
        class="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer"
        @click="toggleDatePicker"
      >
        <CiCalendarDate/>
      </span>
    </div>
  </div>

          <!-- Gender Input -->
          <div class="relative">
            <div class="flex items-center justify-between mb-2">
              <label for="gender" class="block font-bold">Gender</label>
              <div v-if="showErrors.gender" class="text-red-500 text-sm">This field is required</div>
            </div>
            <select
              v-model="formData.gender"
              id="gender"
              :class="darkMode ? 'w-full border border-white rounded p-2 bg-black text-white' : 'w-full border border-black rounded p-2 bg-white text-black'"
              required
            >
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
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
  <textarea
    style="resize: none;"
    class="w-full p-3 border rounded h-80"
    readonly
  >
    Welcome to ProjMan!

    These terms and conditions ("Terms") govern your access to and use of the ProjMan website and services ("Services"). By using our website, you agree to comply with and be bound by these Terms. If you do not agree with these Terms, please do not use the Services.

    1. Acceptance of Terms
    By accessing or using the ProjMan platform, you agree to comply with these Terms, as well as our Privacy Policy. We reserve the right to modify, update, or change these Terms at any time. Any changes will be posted on this page, and the updated Terms will be effective immediately upon posting.

    2. Use of the Service
    ProjMan provides a platform for project management tools, including task management, time tracking, and collaboration features. You agree to:

    Use the Service only for lawful purposes and in accordance with these Terms.
    Not misuse or interfere with the Service in any way.
    Not attempt to gain unauthorized access to the Service, servers, or networks.

    3. Account Registration
    To use certain features of ProjMan, you must create an account. You are responsible for maintaining the confidentiality of your account credentials, and you agree to notify us immediately of any unauthorized use of your account. You must be at least 18 years old to register for an account.

    4. Subscription Plans and Payment
    ProjMan offers both free and paid subscription plans. If you subscribe to a paid plan, you agree to pay the applicable subscription fees in accordance with the plan you choose. Payments are non-refundable, and fees are subject to change. You will be notified of any changes to the fees.

    5. License to Use the Service
    ProjMan grants you a limited, non-exclusive, non-transferable, revocable license to access and use the Service for your internal business or personal use. You may not distribute, modify, or create derivative works based on the Service.

    6. User Content
    You are solely responsible for the content you upload, create, or share through the Service ("User Content"). By uploading or submitting content to ProjMan, you grant us a worldwide, royalty-free, and non-exclusive license to use, display, and distribute the content within the Service.

    7. Privacy
    Your use of the Service is also governed by our Privacy Policy, which outlines how we collect, use, and protect your personal data. Please review our Privacy Policy to understand how your information is handled.

    8. Prohibited Activities
    You agree not to:

    Violate any applicable laws, regulations, or third-party rights.
    Engage in any activity that could harm the Service or other users.
    Use the Service for any illegal or unauthorized purpose, including but not limited to spamming, hacking, or distributing malware.
    Attempt to reverse-engineer, decompile, or disassemble the Service.

    9. Termination
    We reserve the right to suspend or terminate your access to the Service if you violate these Terms or engage in any unlawful activities. You may also terminate your account at any time by contacting us.

    10. Disclaimer of Warranties
    The Service is provided "as is" without any warranties of any kind, either express or implied. We do not guarantee that the Service will be uninterrupted or error-free. You use the Service at your own risk.

    11. Limitation of Liability
    In no event shall ProjMan or its affiliates be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or in connection with your use of the Service.

    12. Indemnification
    You agree to indemnify and hold harmless ProjMan, its affiliates, employees, and partners from any claims, damages, losses, liabilities, or expenses arising from your use of the Service or violation of these Terms.

    13. Governing Law
    These Terms shall be governed by and construed in accordance with the laws of [Your jurisdiction], without regard to its conflict of law principles. Any disputes arising from these Terms shall be resolved in the courts of [Your jurisdiction].

    14. Changes to the Terms
    We may update these Terms at any time. You will be notified of any material changes, and your continued use of the Service after such changes will constitute your acceptance of the new Terms.
  </textarea>

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

  <Button
    v-if="currentStep < steps.length"
    @click="nextStep"
    class="px-4 py-2 border rounded"
    :disabled="isNextDisabled"
  >
    Next
  </Button>

  <Button
    v-if="currentStep === steps.length"
    @click="register"
    class="px-4 py-2 border rounded"
  >
    Register
  </Button>
</div>
    </div>
  </div>
</template>

<script>
import { AkEyeClosed, AkEyeOpen } from "@kalimahapps/vue-icons";
import { IoOutlineMail } from '@kalimahapps/vue-icons';
import { AkPerson } from '@kalimahapps/vue-icons';
import { CiCalendarDate } from '@kalimahapps/vue-icons';
import VueCal from 'vue-cal';

export default {
  components: {
    AkEyeClosed,
    AkEyeOpen,
    IoOutlineMail,
    AkPerson,
    CiCalendarDate,
    VueCal,
  },
  props: {
    text: {
      type: String,
      required: true,
    },
    maxLength: {
      type: Number,
      default: 100,
    },
  },

  data() {
    return {
      isDarkMode: true,
      currentStep: 1,
      steps: ["Account Setup", "Terms and Conditions", "Upload Image"],
      formData: {
        firstName: '',
        lastName: '',
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
        birthday: "",
        gender: "",
        agreeTerms: false,
        profilePicture: null,
        isExpanded: false,
      },

      showErrors: {
        firstName: false,
        lastName: false,
        email: false,
        username: false,
        password: false,
        confirmPassword: false,
        birthday: false,
        gender: false,
        agreeTerms: false,
        profilePicture: false,
      },

      passwordInvalid: false,
      passwordMismatch: false,

      isFieldTouched: {
        firstName: false,
        lastName: false,
        email: false,
        username: false,
        password: false,
        confirmPassword: false,
        birthday: false,
        gender: false,
        agreeTerms: false,
      },
      showDatePicker: false,
      showPassword: false,
      showConfirmPassword: false,
    };
  },
  computed: {
    isTruncatable() {
      return this.text.length > this.maxLength;
    },
    truncatedText() {
      return this.isTruncatable
        ? this.text.slice(0, this.maxLength) + "..."
        : this.text;
    },
    fullText() {
      return this.text;
    },
  },
  watch: {
    "formData.firstName"(value) {
      if (this.isFieldTouched.firstName) {
        this.showErrors.firstName = !value || value.trim().length === 0;
      }
    },
    "formData.lastName"(value) {
      if (this.isFieldTouched.lastName) {
        this.showErrors.lastName = !value || value.trim().length === 0;
      }
    },
    "formData.email"(value) {
      if (this.isFieldTouched.email) {
        this.showErrors.email = !value;
      }
    },
    "formData.username"(value) {
      if (this.isFieldTouched.username) {
        this.showErrors.username = !value;
      }
    },
    "formData.password"(value) {
      if (this.isFieldTouched.password) {
        this.showErrors.password = !value;
        this.passwordInvalid = !this.validatePassword(value);
      }
    },
    "formData.confirmPassword"(value) {
      if (this.isFieldTouched.confirmPassword) {
        this.showErrors.confirmPassword = !value;
        this.passwordMismatch = value !== this.formData.password;
      }
    },
    "formData.birthday"(value) {
      if (this.isFieldTouched.birthday) {
        this.showErrors.birthday = !value;
      }
    },
    "formData.gender"(value) {
      if (this.isFieldTouched.gender) {
        this.showErrors.gender = !value;
      }
    },
    "formData.agreeTerms"(value) {
      if (this.isFieldTouched.agreeTerms) {
        this.showErrors.agreeTerms = !value;
      }
    },
  },
  methods: {
    computed: {
    themeClasses() {
      return this.isDarkMode ? 'bg-black text-white' : 'bg-white text-black';
    },
  },
    togglePassword(field) {
      this[field] = !this[field];
      if (field === "password") {
        this.showPassword = !this.showPassword;
      } else if (field === "confirmPassword") {
        this.showConfirmPassword = !this.showConfirmPassword;
      }
    },
    validateField(field) {
      this.isFieldTouched[field] = true;
      if (!this.formData[field]) {
        this.showErrors[field] = true;
      } else {
        this.showErrors[field] = false;
        if (field === "password") {
          this.passwordInvalid = !this.validatePassword(this.formData.password);
        }
        if (field === "confirmPassword") {
          this.passwordMismatch =
            this.formData.password !== this.formData.confirmPassword;
        }
      }
    },
    validatePassword(password) {
      const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
      return regex.test(password);
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.formData.profilePicture = e.target.result; // Set the image URL as the preview
          this.showErrors.profilePicture = false;
        };
        reader.readAsDataURL(file);
      } else {
        this.showErrors.profilePicture = true;
      }
    },

    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
    },

    nextStep() {
      // Validate current step fields before proceeding
      let valid = true;
      if (this.currentStep === 1) {
        [
          "firstName",
          "lastName",
          "email",
          "username",
          "password",
          "confirmPassword",
          "birthday",
          "gender",
        ].forEach((field) => {
          this.validateField(field);
          if (
            this.showErrors[field] ||
            this.passwordInvalid ||
            this.passwordMismatch
          ) {
            valid = false;
          }
        });
      } else if (this.currentStep === 2) {
        this.validateField("agreeTerms");
        if (this.showErrors.agreeTerms) valid = false;
      }
      if (valid) this.currentStep++;
    },
    prevStep() {
      this.currentStep--;
    },
    toggleText() {
      this.isExpanded = !this.isExpanded;
    },

    async register() {
      try {
        // Validate all fields before making the request
        let valid = true;
        Object.keys(this.formData).forEach((field) => {
          // Skip profilePicture since it's handled differently
          if (field !== 'profilePicture') {
            const fieldValid = this.validateField(field);
            if (!fieldValid || this.showErrors[field]) valid = false;
          }
        });

        // Also check if profilePicture is provided if it's required
        if (!this.formData.profilePicture) {
          this.showErrors.profilePicture = true;
          valid = false;
        }

        if (!valid) {
          alert("Please fill in all required fields correctly.");
          return;
        }

    // Make the API request
    const response = await fetch("http://localhost:8000/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        firstName: this.formData.firstName,
        lastName: this.formData.lastName,
        email: this.formData.email,
        username: this.formData.username,
        password: this.formData.password,
        birthday: this.formData.birthday,
        gender: this.formData.gender,
        profilePicture: this.formData.profilePicture,
      }),
    });

    if (!response.ok) {
      const errorMessage = await response.text();
      console.error("Registration failed:", errorMessage);
      alert("An error occurred during registration: " + errorMessage);
      return;
    }

    const data = await response.json();
    if (data.success) {
      alert("Registration successful! Redirecting to dashboard...");
      this.$router.push("/dashboard"); // Redirect to dashboard
    } else {
      alert("Registration failed: " + (data.error || "Unknown error"));
    }
  } catch (err) {
    console.error("An error occurred during registration:", err);
    alert("An error occurred during registration: " + err.message);
  }
},
    toggleDatePicker() {
      // Trigger the native date picker by clicking the input field programmatically
      const input = this.$refs.birthdayInput;
      if (input) {
        input.showPicker();
      }
    }
   },
};
</script>