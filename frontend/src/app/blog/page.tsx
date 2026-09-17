import Link from "next/link";
import {
  getBlogPosts,
  getFeaturedImageUrl,
  stripHtml,
} from "@/lib/wordpress";

export const revalidate = 0;

export default async function BlogPage() {
  const posts = await getBlogPosts();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Blog</h1>

      {posts.length === 0 ? (
        <p className="text-gray-500">
          Brak wpisow albo WordPress jest jeszcze nieskonfigurowany.
          Sprawdz, czy kontener wordpress dziala i czy opublikowano
          przynajmniej jeden wpis.
        </p>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {posts.map((post) => {
            const image = getFeaturedImageUrl(post);
            const excerpt = stripHtml(post.excerpt.rendered);
            return (
              <Link
                key={post.id}
                href={`/blog/${post.slug}`}
                className="block rounded-lg border bg-white overflow-hidden hover:shadow-md transition-shadow"
              >
                {image && (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={image}
                    alt=""
                    className="w-full h-40 object-cover"
                  />
                )}
                <div className="p-4">
                  <h2
                    className="font-semibold text-lg"
                    dangerouslySetInnerHTML={{ __html: post.title.rendered }}
                  />
                  <p className="mt-2 text-sm text-gray-600 line-clamp-3">
                    {excerpt}
                  </p>
                  <p className="mt-3 text-xs text-gray-400">
                    {new Date(post.date).toLocaleDateString("pl-PL")}
                  </p>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
