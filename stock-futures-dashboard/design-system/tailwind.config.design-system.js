/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      // Futures Watch Brand Colors
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        
        // Futures Watch Custom Colors
        futures: {
          50: '#f0f9ff',   // Light blue background
          100: '#e0f2fe',  // Table header background
          200: '#bae6fd',  // Selected column highlight
          300: '#7dd3fc',  // Hover states
          500: '#3b82f6',  // Primary brand blue
          600: '#2563eb',  // Primary brand blue (darker)
          700: '#1d4ed8',  // Button active state
          900: '#1e3a8a',  // Dark text on light backgrounds
        },
        
        // Financial Data Colors
        profit: {
          positive: '#059669', // Green-600 for positive profits
          negative: '#dc2626', // Red-600 for negative profits
        },
        
        // Status Colors
        status: {
          live: '#10b981',     // Green for live/active data
          refresh: '#f59e0b',  // Amber for refresh indicators
          warning: '#f59e0b',  // Amber for warnings
          error: '#ef4444',    // Red for errors
        },
        
        // Neutral Scale (for tables and UI)
        neutral: {
          0: '#ffffff',
          25: '#fcfcfc',
          50: '#f9fafb',   // Background
          100: '#f3f4f6',  // Table alternating rows
          200: '#e5e7eb',  // Borders
          300: '#d1d5db',  // Input borders
          400: '#9ca3af',  // Placeholder text
          500: '#6b7280',  // Secondary text
          600: '#4b5563',  // Primary text light
          700: '#374151',  // Primary text
          800: '#1f2937',  // Dark text
          900: '#111827',  // Darkest text
        }
      },
      
      // Typography Scale
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],     // 12px - table data, labels
        'sm': ['0.875rem', { lineHeight: '1.25rem' }], // 14px - body text, controls
        'base': ['1rem', { lineHeight: '1.5rem' }],    // 16px - default
        'lg': ['1.125rem', { lineHeight: '1.75rem' }], // 18px - large text
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],  // 20px - headings
        '2xl': ['1.5rem', { lineHeight: '2rem' }],     // 24px - main heading
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }], // 30px - large headings
      },
      
      // Spacing Scale (optimized for dense tables)
      spacing: {
        '0.5': '0.125rem',  // 2px
        '1.5': '0.375rem',  // 6px
        '2.5': '0.625rem',  // 10px
        '3.5': '0.875rem',  // 14px
        '4.5': '1.125rem',  // 18px
        '5.5': '1.375rem',  // 22px
        '6.5': '1.625rem',  // 26px
        '7.5': '1.875rem',  // 30px
        '11': '2.75rem',    // 44px - table row height
        '15': '3.75rem',    // 60px - header height
      },
      
      // Border Radius
      borderRadius: {
        'xs': '0.125rem',   // 2px
        'sm': '0.25rem',    // 4px
        DEFAULT: '0.375rem', // 6px
        'md': '0.375rem',   // 6px
        'lg': '0.5rem',     // 8px
        'xl': '0.75rem',    // 12px
        '2xl': '1rem',      // 16px
      },
      
      // Animation & Transitions
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "pulse-soft": "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in": "fadeIn 0.2s ease-out",
        "slide-in": "slideIn 0.15s ease-out",
      },
      
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(-4px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      
      // Box Shadows
      boxShadow: {
        'xs': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'sm': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'table': '0 1px 3px 0 rgb(0 0 0 / 0.05)',
        'focus': '0 0 0 2px rgb(59 130 246 / 0.5)',
      },
      
      // Screen Breakpoints
      screens: {
        'xs': '375px',   // Mobile
        'sm': '640px',   // Small tablets
        'md': '768px',   // Tablets
        'lg': '1024px',  // Small laptops
        'xl': '1280px',  // Laptops
        '2xl': '1440px', // Desktops
        '3xl': '1920px', // Large desktops
      },
      
      // Z-Index Scale
      zIndex: {
        '60': '60',  // Sticky table headers
        '70': '70',  // Dropdowns
        '80': '80',  // Modals
        '90': '90',  // Tooltips
        '100': '100', // Toasts
      }
    },
  },
  plugins: [require("tailwindcss-animate")],
}
