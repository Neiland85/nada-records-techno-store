import { createComment, getComments } from "@/lib/actions";
import { redirect } from "next/navigation";

// Tipo para comentarios
interface Comment {
  id: number;
  comment: string;
  created_at: string;
}

export default async function Home() {
  // Obtener comentarios existentes
  const commentsResult = await getComments();
  const comments = commentsResult.success ? commentsResult.data : [];

  return (
    <div className="min-h-screen p-8">
      <main className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">
          🎵 Nada Records Techno Store
        </h1>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">💬 Comentarios</h2>

          {/* Formulario para agregar comentarios */}
          <form
            action={async (formData: FormData) => {
              "use server";
              const result = await createComment(formData);
              if (!result.success) {
                // Aquí podrías manejar errores
                console.error(result.message);
              }
              redirect("/");
            }}
            className="mb-6"
          >
            <div className="flex gap-4">
              <input
                type="text"
                name="comment"
                placeholder="Escribe un comentario..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                required
              />
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                Enviar
              </button>
            </div>
          </form>

          {/* Lista de comentarios */}
          <div className="space-y-4">
            {comments && comments.length === 0 ? (
              <p className="text-gray-500 text-center py-8">
                No hay comentarios aún. ¡Sé el primero en comentar!
              </p>
            ) : (
              comments?.map((comment) => (
                <div
                  key={(comment as Comment).id}
                  className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
                >
                  <p className="text-gray-800 dark:text-gray-200">
                    {(comment as Comment).comment}
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    {new Date((comment as Comment).created_at).toLocaleString()}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold mb-4">🎼 Funcionalidades</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li>✅ Base de datos Neon conectada</li>
              <li>✅ Server Actions funcionando</li>
              <li>✅ Vercel Blob para uploads</li>
              <li>✅ Formularios interactivos</li>
              <li>🔄 Próximamente: Sistema de música</li>
            </ul>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold mb-4">🛠️ Tecnologías</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li>⚡ Next.js 15</li>
              <li>🗄️ PostgreSQL (Neon)</li>
              <li>☁️ Vercel Blob Storage</li>
              <li>🎨 Tailwind CSS</li>
              <li>🔐 TypeScript</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
