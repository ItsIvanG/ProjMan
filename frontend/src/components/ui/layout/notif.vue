<template>
  <div
    v-if="isVisible"
    class="fixed top-12 right-4 z-50"
  >
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-black bg-opacity-50"
      @click="closePanel"
    ></div>

    <!-- Notification Panel -->
    <div
      class="relative mt-[25px] mr-[35px] w-[380px] max-h-[500px] rounded-lg bg-black shadow-xl border border-white"
    >
      <!-- Panel Header -->
      <div class="flex items-center justify-between px-4 py-3 border-b border-gray-700">
        <h2 class="text-sm font-medium text-white">Notifications</h2>
        <button @click="closePanel" class="text-gray-400 hover:text-gray-300">
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
      <div class="overflow-y-auto max-h-[450px] divide-y divide-gray-700">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="flex items-start gap-3 px-4 py-3 hover:bg-gray-800 group"
        >
          <!-- Avatar -->
          <Avatar>
            <AvatarImage :src="notification.avatar" />
            <AvatarFallback>{{ notification.initials }}</AvatarFallback>
          </Avatar>

          <!-- Message Content -->
          <div class="flex-1">
            <p
              class="text-sm font-medium"
              :class="notification.unread ? 'text-white' : 'text-gray-400'"
            >
              {{ notification.message }}
            </p>
            <p class="text-sm text-gray-400">{{ notification.body }}</p>
            <p class="text-xs text-gray-500">{{ notification.time }}</p>
          </div>

          <!-- Action Buttons Container -->
          <div class="flex items-center gap-2 p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <!-- Archive Button -->
            <button
              @click="archive(notification.id)"
              class="text-gray-400 hover:text-gray-300 p-2 rounded-full bg-gray-700 hover:bg-gray-600"
            >
              <ReArchiveFill class="h-4 w-5" />
            </button>

            <!-- Unread Button -->
            <button
              @click="toggleUnread(notification.id)"
              class="text-gray-400 hover:text-gray-300 p-2 rounded-full bg-gray-700 hover:bg-gray-600"
            >
              <MdRoundMarkEmailUnread class="h-4 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { ReArchiveFill } from "@kalimahapps/vue-icons";
import { MdRoundMarkEmailUnread } from "@kalimahapps/vue-icons";

export default {
  components: {
    Avatar,
    AvatarImage,
    AvatarFallback,
    ReArchiveFill, // Archive icon
    MdRoundMarkEmailUnread, // Unread icon
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["closePanel"],
  data() {
    return {
      notifications: [
        {
          id: 1,
          avatar: "https://i.pravatar.cc/40?img=1",
          initials: "U1",
          message: "New message from User 1",
          body: "Hey, what's up? All set for the presentation?",
          time: "2 hours ago",
          unread: true,
        },
        {
          id: 2,
          avatar: "https://i.pravatar.cc/40?img=2",
          initials: "U2",
          message: "Meeting Reminder",
          body: "Don't forget the meeting at 3 PM.",
          time: "4 hours ago",
          unread: false,
        },
        {
          id: 3,
          avatar: "https://i.pravatar.cc/40?img=3",
          initials: "U3",
          message: "Code Review Assigned",
          body: "You have been assigned a new code review task.",
          time: "1 day ago",
          unread: true,
        },
        {
          id: 4,
          avatar: "https://i.pravatar.cc/40?img=4",
          initials: "U4",
          message: "Project Deadline Extended",
          body: "The deadline for Project X has been extended.",
          time: "2 days ago",
          unread: false,
        },
        {
          id: 5,
          avatar: "https://i.pravatar.cc/40?img=5",
          initials: "U5",
          message: "New Comment on Issue",
          body: "A new comment has been added to Issue #123.",
          time: "3 days ago",
          unread: false,
        },
        {
          id: 6,
          avatar: "https://i.pravatar.cc/40?img=6",
          initials: "U6",
          message: "Deployment Completed",
          body: "Your latest deployment was successful.",
          time: "4 days ago",
          unread: true,
        },
        {
          id: 7,
          avatar: "https://i.pravatar.cc/40?img=7",
          initials: "U7",
          message: "System Alert",
          body: "There was an error in the system logs.",
          time: "5 days ago",
          unread: false,
        },
        {
          id: 8,
          avatar: "https://i.pravatar.cc/40?img=8",
          initials: "U8",
          message: "Weekly Summary Available",
          body: "Your weekly activity summary is ready.",
          time: "1 week ago",
          unread: true,
        },
      ],
    };
  },
  methods: {
    closePanel() {
      this.$emit("closePanel");
    },

    // Archive a notification
    archive(notificationId) {
      this.notifications = this.notifications.filter(
          (notification) => notification.id !== notificationId
      );
      console.log(`Archived notification with ID ${notificationId}`);
    },

    // Toggle unread status
    toggleUnread(notificationId) {
      const notification = this.notifications.find(
          (notification) => notification.id === notificationId
      );
      if (notification) {
        notification.unread = !notification.unread;
        console.log(
            `Toggled unread status for notification with ID ${notificationId}`
        );
      }
    },
  },
};
</script>

<style scoped>
.max-h-\[450px\]::-webkit-scrollbar {
  width: 6px;
}

.max-h-\[450px\]::-webkit-scrollbar-thumb {
  background-color: #777777; /* Gray */
  border-radius: 4px; /* Round corners for the thumb */
}

.max-h-\[450px\]::-webkit-scrollbar-track {
  background-color: transparent;
  border-radius: 4px; /* Optional: round the corners of the track */
}

/* Ensure the action buttons are hidden initially and only visible on hover */
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}
</style>
