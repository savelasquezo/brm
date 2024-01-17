export const metadata = {
  title: 'BRM',
  description:
    'BRM - Simon Velasquez',
};

export default function ActivateLayout({ children }: { children: React.ReactNode }) {
  return (
    <section>
      {children}
    </section>
  );
}

