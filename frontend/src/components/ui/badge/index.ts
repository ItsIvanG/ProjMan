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
        high: 'border-transparent bg-red-600 text-white hover:bg-red-700',
        low: 'border-transparent bg-blue-600 text-white hover:bg-blue-700',
        medium: 'border-transparent bg-yellow-600 text-white hover:bg-yellow-700',
        veryhigh: 'border-transparent bg-green-800 text-white hover:bg-green-900',  
        leader: 'border-transparent bg-violet-800 text-white hover:bg-violet-900',  
        member: 'border-transparent bg-blue-800 text-white hover:bg-blue-900',
        active: 'border-transparent bg-green-800 text-white hover:bg-green-900', 
        deactivated: 'border-transparent bg-red-600 text-white hover:bg-red-700',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
);

export type BadgeVariants = VariantProps<typeof badgeVariants>;
