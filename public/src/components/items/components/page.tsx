import React, { useEffect, useState } from 'react';
import { Session } from 'next-auth';
import { w3cwebsocket as W3CWebSocket } from 'websocket';

import Image from 'next/image';
import { imageLoader } from '@/utils/imageConfig';

import {AiOutlineClose, AiOutlineShoppingCart} from 'react-icons/ai'
import { GiCheckMark } from "react-icons/gi";


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

interface FormDataItem {
  ammount: string;
  uuid: string;
}

const Header: React.FC<ItemsProps> = ({ session  }) => {
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [listItems, setListItems] = useState<ItemsData[]>([]);

  const [showModal, setShowModal] = useState(false);
  const [closingModal, setClosingModal] = useState(false);

  const openModal = () => {
    setShowModal(true);
  };

  const closeModal = () => {
      setClosingModal(true);
      setTimeout(() => {
          setShowModal(false);
          setClosingModal(false);
      }, 500);
  };

  const [formData, setFormData] = useState<{ [key: string]: FormDataItem }>({});

  const onChange = (e: React.ChangeEvent<HTMLInputElement>, uuid: string) => {
    const newFormData = { ...formData };
    newFormData[uuid] = { ...newFormData[uuid], [e.target.name]: e.target.value };
    setFormData(newFormData);
  };
  

  useEffect(() => {
    const websocketURL = `${process.env.NEXT_PUBLIC_WEBSOCKET_APP}/app/ws/items/`;
    const client = new W3CWebSocket(websocketURL);

    client.onmessage = (message) => {
      let data;
      if (typeof message.data === 'string') {
        data = JSON.parse(message.data);
      }
        setListItems(data);
    }

    return () => {
      if (client.readyState === client.OPEN) {
        client.close();
      }
    };
  },);



  const handleSubmit = async (e: React.FormEvent, listItem: any) => {
    e.preventDefault();
    setSuccess('');
    setError('');

    const email = session?.user?.email
    const uuid = listItem.uuid
    const ammount = formData[listItem.uuid]?.ammount

    const isAmmountValid = /^[0-9]+$/.test(ammount);
    if (!isAmmountValid) {
      setError('¡Error - Ingrese un numero valido!');
      return;
    }

    if (ammount > listItem.ammount) {
      setError("¡Lamentablemente no hay suficiente Inventario!");
      return;
    }

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
        setError('¡Error al Agregar Articulo! Intentelo Nuevamente');
    }
  };

  return (
    <div className="w-full h-full bg-white grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 items-center justify-center py-4 px-8 gap-y-8">
        {listItems.length > 0 ? (
            listItems.map((listItem, i) => (
            <div key={i} className="relative items-center rounded-sm h-full shadow-inner">
                <span className='absolute top-0 flex items-center justify-center text-sm font-semibold text-white bg-gray-800 hover:bg-gray-900 border-slate-950 h-8 w-full uppercase'>{listItem.name}</span>
                <Image loader={imageLoader} width={1240} height={550} src={`${process.env.NEXT_PUBLIC_APP_API_URL}${listItem.banner}`} className="bg-slate-100 mt-8 object-cover rounded-t-sm z-0" alt="" />
                {session && session?.user? (
                  <form className='w-full h-10 flex flex-row justify-between items-center bg-gray-800 hover:bg-gray-900 border-slate-950'>
                    <input
                      className='bg-gray-100 ml-4 text-center rounded-sm outline-0 focus:outline-0 disabled:border-0 w-20'
                      type="text"
                      name="ammount"
                      id={`ammount_${listItem.uuid}`}
                      minLength={1}
                      maxLength={6}
                      value={formData[listItem.uuid]?.ammount || ''}
                      onChange={(e) => onChange(e, listItem.uuid)}
                      required
                    />
                    <button onClick={(event) => {handleSubmit(event, listItem); openModal();}} type='submit' className="flex h-full p-2 items-center justify-between gap-x-2 bg-blue-800 hover:bg-blue-900  border-blue-950 transition-colors duration-300">
                        <span className='text-white font-semibold text-md'><AiOutlineShoppingCart /></span>
                        <span className="block text-white shadow-inner text-xs uppercase font-semibold">
                            Agregar
                        </span>
                    </button>
                  </form>
                ) : (
                  <div className='flex flex-row justify-between items-center bg-gray-800 hover:bg-gray-900 border-slate-950 h-12 w-full'></div>
                )}
            </div>
            ))
            ) : (
            <div className="relative flex flex-col items-center rounded-sm h-40 md:h-80 shadow-inner">
              <p>Cargado Articulos</p>
            </div>
          )}
          {showModal && (
          <div className={`fixed top-0 left-0 w-full h-full flex items-center justify-center transition bg-opacity-50 bg-gray-900 backdrop-blur-sm z-40 ${closingModal ? "animate-fade-out animate__animated animate__fadeOut" : "animate-fade-in animate__animated animate__fadeIn"}`}>
              <div className="w-1/3 h-14 px-4 bg-gray-800 rounded-lg flex flex-row-reverse items-center justify-between">
                <button onClick={closeModal} className='text-xl text-gray-400 hover:text-gray-600 transition-colors duration-300' ><AiOutlineClose /></button>
                {error && (
                <div className="flex flex-row items-center gap-2 text-red-400 text-sm">
                  <span className='text-lg'><AiOutlineClose /></span>
                  {error}
                </div>)}
                {success && (
                <div className="flex flex-row gap-2 items-center text-green-400 text-sm">
                  <span className='text-lg'><GiCheckMark /></span>
                  {success}
                </div>)}
                {!error && !success && (<div className="text-gray-400 text-xs mt-2 h-6">¿Necesitas Ayuda? support@brm.com</div>)}
              </div>
            </div>
        )}
    </div>
);
};

export default Header;