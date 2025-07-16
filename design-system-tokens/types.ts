/**
 * Nuru AI Design Tokens - Type Definitions
 * Generated automatically from design system tokens - DO NOT EDIT MANUALLY
 */

export interface ColorScale {
  50: string;
  100: string;
  200: string;
  300: string;
  400: string;
  500: string;
  600: string;
  700: string;
  800: string;
  900: string;
  950?: string;
}

export interface ColorTokens {
  primary: ColorScale;
  secondary: ColorScale;
  neutral: ColorScale;
  success: ColorScale;
  warning: ColorScale;
  error: ColorScale;
  info: ColorScale;
  amber: ColorScale;
  violet: ColorScale;
  emerald: ColorScale;
  semantic?: {
    background: Record<string, string>;
    text: Record<string, string>;
    border: Record<string, string>;
    brand: Record<string, string>;
  };
  darkMode?: {
    neutral: ColorScale;
  };
}

export interface SpacingTokens {
  spacing?: Record<string, string>;
  semantic?: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
    '3xl': string;
    component: {
      padding: string;
      margin: string;
      gap: string;
    };
  };
}

export interface TypographyTokens {
  fontFamily?: {
    sans: string;
    mono: string;
    heading: string;
  };
  fontSize?: Record<string, string>;
  lineHeight?: Record<string, string>;
  fontWeight?: Record<string, string>;
  letterSpacing?: Record<string, string>;
  semantic?: {
    heading: Record<string, Record<string, string>>;
    body: Record<string, Record<string, string>>;
  };
}

export interface ComponentTokens {
  components?: Record<string, Record<string, any>>;
  variants?: Record<string, Record<string, Record<string, any>>>;
}

export interface DesignTokens {
  colors?: ColorTokens;
  spacing?: SpacingTokens;
  typography?: TypographyTokens;
  components?: ComponentTokens;
}

// Utility types for token paths
export type ColorPath =
  | `primary.${keyof ColorScale}`
  | `secondary.${keyof ColorScale}`
  | `neutral.${keyof ColorScale}`
  | `success.${keyof ColorScale}`
  | `warning.${keyof ColorScale}`
  | `error.${keyof ColorScale}`
  | `info.${keyof ColorScale}`
  | `amber.${keyof ColorScale}`
  | `violet.${keyof ColorScale}`
  | `emerald.${keyof ColorScale}`;

export type SpacingKey = string;
export type FontSizeKey = string;
export type FontWeightKey = string;

// Component variant types
export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost';
export type BadgeVariant = 'default' | 'primary' | 'success' | 'warning' | 'error';
export type ComponentSize = 'sm' | 'md' | 'lg';
