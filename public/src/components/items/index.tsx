import { useSession } from 'next-auth/react';
import Items from './components/page';

export default function Page() {
  const { data: session } = useSession();
  return (
    <section>
      <Items session={session} />
    </section>
  );
}

