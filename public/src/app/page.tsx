'use client';

import dotenv from 'dotenv';
dotenv.config();

import React from 'react';
import { SessionProvider } from 'next-auth/react';

import Header from '@/components/header/index';
import Items from '@/components/items/index';

export default function Home() {
  return (
    <SessionProvider>
      <Header />
      <main className='w-full h-full'>
        <Items />
      </main>
    </SessionProvider>
  );
}