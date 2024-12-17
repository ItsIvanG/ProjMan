<template>
  <div
    v-if="isVisible"
    class="fixed top-12 right-4 z-50"
  >
    <!-- Backdrop -->
    <div
      class="fixed inset-0  bg-opacity-50"
      @click="closePanel"
    ></div>

    <!-- Notification Panel -->
    <div
      class="relative mt-[25px] mr-[35px] w-[380px] max-h-[500px] rounded-lg  shadow-xl border bg-white dark:bg-black"
    >
      <!-- Panel Header -->
      <div class="flex items-center justify-between px-4 py-3 border-b ">
        <h2 class="text-sm font-medium ">Notifications</h2>
        <button @click="closePanel" class="">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Notifications List -->
      <div class="overflow-y-auto max-h-[450px] divide-y ">
        <div
          v-for="notification in notifications"
          :key="notification.notification_id"
          class="flex items-start gap-3 px-4 py-3  group"
        >
          <!-- Avatar -->
          <Avatar>
            <AvatarImage  :src="`http://localhost:8000/media/${notification.notification_user_created_picture}`"
 />
            <AvatarFallback><User/></AvatarFallback>
          </Avatar>

          <!-- Message Content -->
          <div class="flex-1">
            <p
              class="text-sm font-medium">
              <!--              :class="notification.unread ? 'text-white' : 'text-gray-400'"-->

              {{ notification.notification_user_created_name }}
            </p>
            <p class="text-sm ">{{ notification.notification_content }}</p>
            <p class="text-xs ">{{ formatDate(notification.notification_datetime) }}</p>
          </div>

          <!-- Action Buttons Container -->
          <div class="flex items-center gap-2 p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <!-- Archive Button -->
            <button
             @click="deleteNotification(notification.notification_id)"
            >
              <X class="h-4 w-5" />
            </button>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import {User, X} from "lucide-vue-next";
import { MdRoundMarkEmailUnread } from "@kalimahapps/vue-icons";
import {getAPI} from "@/axios.ts";
import { useAuthStore } from '@/store/auth'
import {useProjectStore} from "@/store/project.ts";

const authStore = useAuthStore();
const projectStore = useProjectStore();
// Props
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false,
  },
});

// Emits
const emitClosePanel = defineEmits(["closePanel"]);

// State
const notifications = ref([
  {
    notification_id: 1,
    notification_user_created_picture: "",
    notification_user_created_name: "",
    notification_content: "",
    notification_datetime: "",
  },
]);

// Methods
const closePanel = () => {
  emitClosePanel("closePanel");
};

// Archive a notification
const archive = (notificationId: number) => {
  notifications.value = notifications.value.filter(
    (notification) => notification.notification_id !== notificationId
  );
  console.log(`Archived notification with ID ${notificationId}`);
};
const userId = computed(() => authStore.user?.id);

const fetchNotifications = async () => {

  try {
    const response = await getAPI.get('/api/notifications/', {
      params: {
        user: userId.value, // Query parameter to filter by user ID
        project_id: projectStore?.project_id
      },
    });
    notifications.value = response.data;
  } catch (err) {
    console.error('Error fetching notifications:', err);
  }
};
onMounted(() => {
  fetchNotifications();
});

function formatDate(dateString: string): string {
  const date = new Date(dateString);

  // Get the components
  const options: Intl.DateTimeFormatOptions = {
    month: '2-digit',
    day: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  };

  return date.toLocaleString('en-US', options);
}

const deleteNotification = async (notificationId: number) => {
  try {
    await getAPI.delete(`/api/notifications/${notificationId}/`);
    archive(notificationId)
    console.log(`Deleted notification with ID ${notificationId}`);
  } catch (error) {
    console.error("Failed to delete notification:", error);
  }
}
</script>
