import React from 'react';
import { Session } from 'next-auth';
import Image from 'next/image';
import Link from 'next/link';

import Auth from '@/components/auth/components/page';

type FooterProps = {};

const Footer: React.FC<FooterProps> = () => {
  return (
    <footer className="absolute bottom-0 w-full bg-gray-900 px-4 lg:px-2 py-2.5">
    <div className="flex flex-col justify-center items-start mx-auto max-w-screen-xl">
        <p className='text-white font-thin text-xs'>Simon Velasquez - Fullstack Developer Django/NextJs</p>
        <p className='text-white font-thin text-xs'>Test: Desarrollador Líder Fullstack</p>
    </div>
  </footer>
  );
};

export default Footer;