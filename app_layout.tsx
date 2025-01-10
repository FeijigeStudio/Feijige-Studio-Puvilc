import React from 'react';
import { ReactNode } from 'react';
import LanguageSwitcher from './components/LanguageSwitcher';

interface RootLayoutProps {
  children: ReactNode;
}

const RootLayout: React.FC<RootLayoutProps> = ({ children }) => {
  return (
    <html lang="en">
      <body>
        <LanguageSwitcher />
        {children}
      </body>
    </html>
  );
};

export default RootLayout;

