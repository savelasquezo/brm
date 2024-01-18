import React, { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Session } from 'next-auth';
import { signOut } from 'next-auth/react';
import { NextResponse } from 'next/server';

import LoginModal from "./loginModal";
import RegisterModal from "./registerModal";
import ForgotPasswordModal from "./ForgotPasswordModal";
import ForgotPasswordConfirmModal from "./ForgotPasswordConfirmModal";
import CircleLoader from 'react-spinners/CircleLoader';

import {AiOutlineClose, AiFillLock, AiFillUnlock, AiOutlineShoppingCart} from 'react-icons/ai'

type AuthProps = {
  session: Session | null | undefined;
};

interface ShopCartData {
  id: number;
  last_updated: string;
  total: number;
  user: string;
  items: CartItemData[];
}

interface ItemDetails {
  uuid: string;
  lot_number: string;
  name: string;
  price: number;
  ammount: number;
  banner: string;
  date_joined: string;
  is_active: boolean;
}

interface CartItemData {
  id: number;
  price: number;
  ammount: number;
  shoppcart: number;
  item: number;
  details: ItemDetails;
}

export const fetchShopCart = async () => {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_APP_API_URL}/app/user/fetch-shopcart/`,{
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


const Auth: React.FC<AuthProps> = ({ session  }) => {
    const searchParams = useSearchParams();
    const router = useRouter();

    const [loading, setLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [closingModal, setClosingModal] = useState(false);
    
    const [showForgotPasswordModal, setShowForgotPasswordModal] = useState(false);
    const [shopCart, setShopCart] = useState<ShopCartData | null>(null);

    const updateForgotPasswordModalState = (value: boolean): void => {
      setShowForgotPasswordModal(value);
    };
  
    const [activeTab, setActiveTab] = useState('login');
    const [activeCartTab, setActiveCartTab] = useState('cart');
  
    useEffect(() => {
      if (searchParams.get('login')) {
        setShowModal(true);
        setActiveTab('login');
      }
      if (searchParams.get('singup')) {
        setShowModal(true);
        setActiveTab('singup');
      }
      if (searchParams.get('forgot_password_confirm')) {
        setShowModal(true);
        setShowForgotPasswordModal(true);
        setActiveTab('forgot_password_confirm');
      }

      fetchShopCart()
        .then((data) => {
          setShopCart(data);
        })
        .catch((error) => {
          console.error('Error al obtener datos iniciales de imagenSliders:', error);
        });

    }, [searchParams]);

    
    const openModal = (tab: string) => {
      setShowModal(true);
      setActiveTab(tab);
    };

    const openCartModal = (tab: string) => {
      setShowModal(true);
      setActiveCartTab(tab);
    };
  
    const closeModal = () => {
      setClosingModal(true);
      setTimeout(() => {
        setShowModal(false);
        setClosingModal(false);
        router.push('/');
      }, 500);
    };

    return (
        <main className="inline-flex items-center h-full ml-5 lg:w-2/5 lg:justify-end lg:ml-0 gap-x-3">
            {session && session?.user? (
              <div className='inline-flex gap-x-4'>
                <button onClick={() => openModal('shopcart')}  className="bg-blue-500 hover:bg-blue-700 text-white uppercase text-xs font-semibold p-2 rounded transition-colors duration-300">
                  <span className='flex flex-row text-lg items-center justify-between h-4 gap-x-2'>
                    <AiOutlineShoppingCart /> 
                    <span className='text-sm'>({shopCart?.items?.length ?? ""})</span>
                  </span>
                </button>
                <button onClick={() => {signOut();}} className="bg-pink-700 hover:bg-pink-900 text-white uppercase text-xs font-semibold p-2 rounded transition-colors duration-300">Salir</button>
              </div>
              ) : (
              <div className='inline-flex gap-x-2'>
                <button onClick={() => openModal('login')} className="bg-red-500 hover:bg-red-700 text-white text-sm font-semibold py-1 px-2 rounded transition-colors duration-300">Ingresar</button>
                <button onClick={() => openModal('singup')} className="bg-pink-700 hover:bg-pink-900 text-white text-sm font-semibold py-1 px-2 rounded transition-colors duration-300">Inscribirse</button>
              </div>
            )}
            {showModal && activeTab !== 'shopcart' && (
            <div className={`fixed top-0 left-0 w-full h-full flex items-center justify-center transition bg-opacity-50 bg-gray-900 backdrop-blur-sm z-40 ${closingModal ? "animate-fade-out animate__animated animate__fadeOut" : "animate-fade-in animate__animated animate__fadeIn"}`}>
                <div className="relative w-1/4 flex h-3/4">
                  <button onClick={closeModal} className='absolute top-4 right-4 text-xl text-gray-400 hover:text-gray-600 transition-colors duration-300' ><AiOutlineClose /></button>
                  <div className="w-full h-full bg-gray-800 rounded-2xl p-6">
                    <div className='flex flex-row w-full items-center'>
                      <button onClick={() => openModal('login')} className={`text-gray-100 rounded-full px-4 py-1 inline-flex text-sm font-semibold transition duration-300 mr-2 ${activeTab === 'login' ?  'bg-red-500 hover:bg-red-600' : ''}`}>Ingresar</button>
                      <button onClick={() => openModal('singup')} className={`text-gray-100 rounded-full px-4 py-1 inline-flex text-sm font-semibold transition duration-300 mr-2 ${activeTab === 'singup' ? 'bg-pink-700 hover:bg-pink-800' : ''}`}>Inscribirse</button>
                      {showForgotPasswordModal ? (
                        <button onClick={() => openModal('forgot_password_confirm')} className={`text-gray-100 rounded-full px-2 py-1 inline-flex text-sm font-semibold transition duration-300 mr-2 ${activeTab === 'forgot_password_confirm' ? 'bg-green-600 hover:bg-green-700' : ''}`}><AiFillUnlock/></button>
                        ) : (
                        <button onClick={() => openModal('forgot-password')} className={`text-gray-100 rounded-full px-2 py-1 inline-flex text-sm font-semibold transition duration-300 mr-2 ${activeTab === 'forgot-password' ? 'bg-yellow-600 hover:bg-yellow-700' : ''}`}><AiFillLock/></button>
                        )}
                    </div>
                    <div className={`h-full my-4 ${activeTab === 'login' ? 'block animate-fade-in animate__animated animate__fadeIn' : 'hidden animate-fade-out animate__animated animate__fadeOut'}`}>
                      <LoginModal closeModal={closeModal}/>
                      <div className="text-start items-center inline-flex gap-x-2">
                        <p className="text-xs text-gray-300">¿No tienes una cuenta?</p>
                        <button onClick={() => openModal('singup')} className="cursor-pointer text-red-500 hover:text-pink-600 transition-colors duration-300 -mt-1">Inscribete</button>
                      </div><br />
                      <button onClick={() => openModal('forgot-password')} className="hover:underline text-xs text-blue-500">¿Olvidaste la contraseña?</button>
                    </div>
                    <div className={`h-full my-4 ${activeTab === 'singup' ? 'block animate-fade-in animate__animated animate__fadeIn' : 'hidden animate-fade-out animate__animated animate__fadeOut'}`}>
                      <RegisterModal closeModal={closeModal}/>
                      <div className="inline-flex gap-x-2 items-center">
                        <p className="text-xs text-gray-300">¿Ya tienes una cuenta?</p>
                        <button onClick={() => openModal('login')} className="cursor-pointer text-red-500 hover:text-pink-600 transition-colors duration-300 -mt-1">Ingresar</button>
                      </div>
                    </div>
                    <div className={`h-full my-4 ${activeTab === 'forgot-password' ? 'block animate-fade-in animate__animated animate__fadeIn' : 'hidden animate-fade-out animate__animated animate__fadeOut'}`}>
                      <ForgotPasswordModal closeModal={closeModal}/>
                      <div className="inline-flex gap-x-2 items-center">
                        <p className="text-xs text-gray-300">¿Ya tienes una cuenta?</p>
                        <button onClick={() => openModal('login')} className="cursor-pointer text-red-500 hover:text-pink-600 transition-colors duration-300 -mt-1">Ingresar</button>
                      </div>
                    </div>
                    <div className={`h-full my-4 ${activeTab === 'forgot_password_confirm' ? 'block animate-fade-in animate__animated animate__fadeIn' : 'hidden animate-fade-out animate__animated animate__fadeOut'}`}>
                      <ForgotPasswordConfirmModal closeModal={closeModal} updateForgotPasswordModalState={updateForgotPasswordModalState}/>
                      <div className="inline-flex gap-x-2 items-center">
                        <p className="text-xs text-gray-300">¿Ya tienes una cuenta?</p>
                        <button onClick={() => openModal('login')} className="cursor-pointer text-red-500 hover:text-pink-600 transition-colors duration-300 -mt-1">Ingresar</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
          )}
          {showModal && activeTab === 'shopcart' && (
            <div className={`fixed top-0 left-0 w-full h-full flex items-center justify-center transition bg-opacity-50 bg-gray-900 backdrop-blur-sm z-40 ${closingModal ? "animate-fade-out animate__animated animate__fadeOut" : "animate-fade-in animate__animated animate__fadeIn"}`}>
              <div className="relative w-1/3 h-3/4">
                <button onClick={closeModal} className='absolute top-4 right-4 text-xl text-gray-400 hover:text-gray-600 transition-colors duration-300' ><AiOutlineClose /></button>
                <div className="w-full h-full bg-gray-800 rounded-2xl p-6">
                  <div className='flex flex-row w-full items-center'>
                      <button onClick={() => openCartModal('cart')} className={`text-gray-100 rounded-md px-2 py-0.5 inline-flex text-sm font-semibold transition duration-300 mr-2 ${activeCartTab === 'cart' ?  'bg-blue-500 hover:bg-blue-600' : ''}`}>Carrito</button>
                      <button onClick={() => openCartModal('invoice')} className={`text-gray-100 rounded-md px-2 py-0.5 inline-flex text-sm font-semibold transition duration-300 mr-2 ${activeCartTab === 'invoice' ? 'bg-yellow-700 hover:bg-yellow-800' : ''}`}>Historial</button>
                  </div>
                  <div className={`h-full my-4 flex flex-col justify-start items-center px-4 py-2 ${activeCartTab === 'cart' ? 'block animate-fade-in animate__animated animate__fadeIn' : 'hidden animate-fade-out animate__animated animate__fadeOut'}`}>
                    {shopCart && (
                      <div key={shopCart.id} className='relative w-full h-full flex flex-col'>
                        <span className='flex flex-row justify-between my-2'>
                          <span className='flex flex-col justify-center items-start'>
                            <p className='font-semibold text-sm text-gray-200'>CARRITO DE COMPRA</p>
                            <p className='text-xs text-gray-400'>{shopCart.user}</p>
                          </span>
                          <p className='text-gray-400'>{shopCart.last_updated}</p>
                        </span>
                        {shopCart.items.length > 0 && (
                        <table className="min-w-full text-center text-sm font-light my-4">
                          <thead className="font-medium text-white">
                            <tr className="border-b border-slate-900 uppercase text-xs">
                              <th scope="col" className=" px-2 py-1 text-left">Nombre</th>
                              <th scope="col" className=" px-2 py-1">Lote</th>
                              <th scope="col" className=" px-2 py-1">Precio</th>
                              <th scope="col" className=" px-2 py-1">Cantidad</th>
                              <th scope="col" className=" px-2 py-1">Subtotal</th>
                            </tr>
                          </thead>
                          {shopCart.items.map((item) => (
                            <tr key={item.id} className="border-b border-slate-700 uppercase text-xs text-white">
                              <td className="whitespace-nowrap px-2 py-1 text-xs capitalize text-left">{item.details.name}</td>
                              <td className="whitespace-nowrap px-2 py-1">{item.details.lot_number}</td>
                              <td className="whitespace-nowrap px-2 py-1">{item.price.toLocaleString()}</td>
                              <td className="whitespace-nowrap px-2 py-1">{item.ammount}</td>
                              <td className="whitespace-nowrap px-2 py-1">{(item.ammount*item.price).toLocaleString()}</td>
                            </tr>
                          ))}
                        </table>
                        )}
                        <div className='absolute bottom-10 w-full flex flex-col gap-y-4'>
                          <span className='flex flex-row justify-between items-center'>
                            <p className='text-gray-400 text-sm'>Total (IVA incl.):</p>
                            <p className='text-white font-semibold text-sm'>${shopCart.total.toLocaleString()} (COP)</p>
                          </span>
                          {loading ? (
                            <button type="button" className="bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md py-2 px-4 w-full text-center flex items-center justify-center">
                              <CircleLoader loading={loading} size={25} color="#1c1d1f" />
                            </button>
                          ) : (
                            <button type="submit" className="bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md py-2 px-4 w-full text-center">Confirmar</button>
                          )}
                        </div>                                           
                      </div>
                    )}
                  </div>
                  <div className={`h-full my-4 flex flex-col justify-start items-center px-4 py-2 ${activeCartTab === 'invoice' ? 'block animate-fade-in animate__animated animate__fadeIn' : 'hidden animate-fade-out animate__animated animate__fadeOut'}`}>
                      <p>Facturas</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
    );
};

export default Auth