/**
 * Nuru AI Design System - React Theme Provider
 * Generated automatically from design system tokens - DO NOT EDIT MANUALLY
 */

import React, { createContext, useContext, useEffect } from 'react';
import { tokens } from '../js/tokens';

interface ThemeContextType {
  tokens: typeof tokens;
  getColor: (path: string) => string | undefined;
  getSpacing: (key: string) => string | undefined;
  getCSSVar: (category: string, ...keys: string[]) => string;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export interface ThemeProviderProps {
  children: React.ReactNode;
  injectCSS?: boolean;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({
  children,
  injectCSS = true
}) => {
  useEffect(() => {
    if (injectCSS) {
      // Inject CSS custom properties into document head
      const styleId = 'nuru-design-tokens';
      const existingStyle = document.getElementById(styleId);

      if (!existingStyle) {
        const style = document.createElement('style');
        style.id = styleId;

        // Import the CSS tokens
        import('../css/design-tokens.css').then((cssModule) => {
          style.textContent = cssModule.default || '';
          document.head.appendChild(style);
        });
      }
    }
  }, [injectCSS]);

  const getColor = (path: string): string | undefined => {
    const keys = path.split('.');
    let value: any = tokens.colors;
    for (const key of keys) {
      value = value?.[key];
      if (value === undefined) return undefined;
    }
    return value;
  };

  const getSpacing = (key: string): string | undefined => {
    return (tokens.spacing as any)?.spacing?.[key] || (tokens.spacing as any)?.[key];
  };

  const getCSSVar = (category: string, ...keys: string[]): string => {
    const path = [category, ...keys].join('-');
    return `var(--${path})`;
  };

  const contextValue: ThemeContextType = {
    tokens,
    getColor,
    getSpacing,
    getCSSVar
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Utility hooks for common token access
export const useColors = () => {
  const { tokens } = useTheme();
  return tokens.colors || {};
};

export const useSpacing = () => {
  const { tokens } = useTheme();
  return tokens.spacing || {};
};

export const useTypography = () => {
  const { tokens } = useTheme();
  return tokens.typography || {};
};

// Higher-order component for theme injection
export function withTheme<P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P & { theme?: ThemeContextType }> {
  return function ThemedComponent(props: P & { theme?: ThemeContextType }) {
    const theme = useTheme();
    return <Component {...props} theme={theme} />;
  };
}

export default ThemeProvider;
