import React, { useEffect, useState } from 'react';
import { Session } from 'next-auth';
import Image from 'next/image';
import Link from 'next/link';
import { NextResponse } from 'next/server';

import {AiOutlineClose, AiOutlineShoppingCart} from 'react-icons/ai'

type ItemsProps = {
  session: Session | null | undefined;
};

interface ItemsData {
  uuid: string;
  name: string;
  price: number;
  ammount: number;
  banner: string;
}

export const fetchItems = async () => {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_APP_API_URL}/app/items/fetch-items/`,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      },
    );
    if (!res.ok) {
      return NextResponse.json({ error: 'Server responded with an error' });
    }
    const data = await res.json();
    return data;
  } catch (error) {
    return NextResponse.json({ error: 'There was an error with the network request' });
  }
}

const Header: React.FC<ItemsProps> = ({ session  }) => {

  const [showModal, setShowModal] = useState(false);
  const [closingModal, setClosingModal] = useState(false);

  const [activeTab, setActiveTab] = useState('');
  const [itemId, setItemId] = useState<any>('');

  const openModal = (tab: string, itemId: any) => {
    setItemId(itemId);
    setShowModal(true);
    setActiveTab(tab);
  };

  const closeModal = () => {
      setClosingModal(true);
      setTimeout(() => {
          setShowModal(false);
          setClosingModal(false);
      }, 500);
  };

  const [listItems, setListItems] = useState<ItemsData[]>([]);
  useEffect(() => {
    fetchItems()
      .then((data) => {
        setListItems(data);
      })
      .catch((error) => {
        console.error('Error fetching Items:', error);
      });
  }, []);

  return (
    <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-4 items-center justify-center py-4">
        {listItems.length > 0 ? (
            listItems.map((listItem, i) => (
            <div key={i} className="relative flex flex-col items-center rounded-sm h-40 md:h-80 shadow-inner">
                <Image unoptimized width={1240} height={550} src={listItem.banner} className="absolute top-0 left-0 h-[calc(100%-16px)] w-full object-cover rounded-t-sm z-0" alt="" />
                <button onClick={() => openModal('buyTicket', listItem.uuid)} className="absolute bottom-5 right-2 flex items-center justify-between gap-x-2 bg-gray-800 hover:bg-gray-900  border-slate-950 transition-colors duration-300 px-4 py-2 rounded border-b-2">
                    <span className='text-white font-semibold text-md'><AiOutlineShoppingCart /></span>
                    <span className="block text-white shadow-inner text-xs uppercase font-semibold">
                        Comprar
                    </span>
                </button>
            </div>
            ))
            ) : (
            <div className="relative flex flex-col items-center rounded-sm h-40 md:h-80 shadow-inner">
              <p>No hay productos disponibles</p>
            </div>
          )}
        

    </div>
);
};

export default Header;