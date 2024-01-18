
import 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: {
      username: string;
      email: string;
      city: string;
      street: string;
      accessToken: string;
      refreshToken: string;
    };
  }
}