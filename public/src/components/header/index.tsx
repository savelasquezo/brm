import { useSession } from 'next-auth/react';
import Header from './components/page';

export default function Page() {
  const { data: session } = useSession();
  return (
    <section>
      <Header session={session} />
    </section>
  );
}


