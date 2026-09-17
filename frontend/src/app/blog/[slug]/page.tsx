import { notFound } from "next/navigation";
import {
  getAuthorName,
  getBlogPostBySlug,
  getFeaturedImageUrl,
} from "@/lib/wordpress";

export const revalidate = 0;

export default async function BlogPostPage({
  params,
}: {
  params: { slug: string };
}) {
  const post = await getBlogPostBySlug(params.slug);
  if (!post) notFound();

  const image = getFeaturedImageUrl(post);
  const author = getAuthorName(post);

  return (
    <article className="space-y-6 max-w-3xl">
      <div>
        <h1
          className="text-2xl font-bold"
          dangerouslySetInnerHTML={{ __html: post.title.rendered }}
        />
        <p className="text-sm text-gray-500 mt-1">
          {new Date(post.date).toLocaleDateString("pl-PL")}
          {author ? ` - ${author}` : ""}
        </p>
      </div>

      {image && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={image} alt="" className="w-full rounded-lg" />
      )}

      <div
        className="prose max-w-none"
        dangerouslySetInnerHTML={{ __html: post.content.rendered }}
      />
    </article>
  );
}
