import React, { useEffect, useState } from 'react';
import { Session } from 'next-auth';
import { NextResponse } from 'next/server';

import Link from 'next/link';
import Image from 'next/image';
import { imageLoader } from '@/utils/imageConfig';

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
    const res = await fetch(`${process.env.NEXT_PUBLIC_APP_API_URL}/app/item/fetch-items/`,{
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
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

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

  const [formData, setFormData] = useState({
    email: session?.user?.email || '',
    uuid: '',
    ammount: '',
  });

  const {email, uuid, ammount } = formData;
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, [e.target.name]: e.target.value });

  useEffect(() => {
    fetchItems()
      .then((data) => {
        setListItems(data);
      })
      .catch((error) => {
        console.error('Error fetching Items:', error);
      });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_APP_API_URL}/app/user/add-item-shopcart/`, 
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `JWT ${session?.user?.accessToken}`,
        },
        body: JSON.stringify({    
          email,
          uuid,
          ammount,
        }),
      });
      const data = await res.json();
      if (!data.error) {
        setSuccess('¡Articulo agregado al carrito!');
      }
    } catch (error) {
      return NextResponse.json({ error: 'There was an error with the network request' });
    }
  };

  return (
    <div className="w-full grid grid-cols-2 md:grid-cols-4 gap-4 items-center justify-center py-4">
        {listItems.length > 0 ? (
            listItems.map((listItem, i) => (
            <div key={i} className="items-center rounded-sm h-40 md:h-80 shadow-inner">
                <Image loader={imageLoader} width={1240} height={550} src={listItem.banner} className="h-[calc(100%-16px)] w-full object-cover rounded-t-sm z-0 bg-red-400" alt="" />
                <form className='flex flex-row justify-between items-center bg-gray-800 hover:bg-gray-900 border-slate-950 h-12 w-full px-4 py-1'>
                  <input className='bg-white'
                    type="number"
                    name="ammount"
                    id="ammount"
                    minLength={1}
                    onChange={(e) => onChange(e)}
                    required
                  />
                  <input type="hiden" name="uuid" id="uuid" value={listItem.uuid} required/>
                  <button onClick={handleSubmit} type='submit' className="flex items-center justify-between gap-x-2 bg-blue-800 hover:bg-blue-900  border-blue-950 transition-colors duration-300 px-2 py-0.5 rounded border-b-2 h-8">
                      <span className='text-white font-semibold text-md'><AiOutlineShoppingCart /></span>
                      <span className="block text-white shadow-inner text-xs uppercase font-semibold">
                          Agregar
                      </span>
                  </button>
                </form>
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