import { cva, type VariantProps } from 'class-variance-authority';

export { default as Badge } from './Badge.vue';

export const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
        secondary: 'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        destructive: 'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
        outline: 'text-foreground',
        notStarted: 'border-transparent bg-red-600 text-white hover:bg-red-700',
        inProgress: 'border-transparent bg-blue-600 text-white hover:bg-blue-700',
        completed: 'border-transparent bg-green-800 text-white hover:bg-green-900', 
        cancelled: 'border-transparent bg-yellow-600 text-white hover:bg-yellow-700', 
        high: 'border-transparent bg-orange-700 text-white hover:bg-orange-800',
        low: 'border-transparent bg-green-800 text-white hover:bg-green-900',
        medium: 'border-transparent bg-blue-600 text-white hover:bg-blue-700',
        veryhigh: 'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',    
        manager: 'border-transparent bg-violet-800 text-white hover:bg-violet-900',  
        member: 'border-transparent bg-blue-800 text-white hover:bg-blue-900',
        active: 'border-transparent bg-green-800 text-white hover:bg-green-900', 
        archived: 'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
        sprint1: 'border-transparent bg-teal-800 text-white hover:bg-teal-900',
        sprint2: 'border-transparent bg-indigo-800 text-white hover:bg-indigo-900',
        sprint3: 'border-transparent bg-orange-800 text-white hover:bg-orange-900',
        sprint4: 'border-transparent bg-lime-800 text-white hover:bg-lime-900',
        sprint5: 'border-transparent bg-cyan-800 text-white hover:bg-cyan-900',
        sprint6: 'border-transparent bg-rose-800 text-white hover:bg-rose-900',
        sprint7: 'border-transparent bg-amber-800 text-white hover:bg-amber-900',
        sprint8: 'border-transparent bg-purple-800 text-white hover:bg-purple-900',
        sprint9: 'border-transparent bg-pink-800 text-white hover:bg-pink-900',
        sprint10: 'border-transparent bg-gray-800 text-white hover:bg-gray-900',
        sprint11: 'border-transparent bg-stone-800 text-white hover:bg-stone-900',
        sprint12: 'border-transparent bg-emerald-800 text-white hover:bg-emerald-900',
        sprint13: 'border-transparent bg-sky-800 text-white hover:bg-sky-900',
        sprint14: 'border-transparent bg-fuchsia-800 text-white hover:bg-fuchsia-900',
        sprint15: 'border-transparent bg-yellow-800 text-white hover:bg-yellow-900',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
);

export type BadgeVariants = VariantProps<typeof badgeVariants>;
