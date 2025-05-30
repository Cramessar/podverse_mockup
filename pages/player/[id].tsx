import { useRouter } from "next/router";

export default function PlayerPage() {
  const router = useRouter();
  const { id } = router.query;

  if (!id) return <div>Loading...</div>;

  return (
    <main className="p-6">
      <h1 className="text-3xl font-bold mb-4">Podcast Player</h1>
      <p>Now playing podcast with ID: <strong>{id}</strong></p>
      {/* TODO: Add audio player and episode/show details here */}
    </main>
  );
}
