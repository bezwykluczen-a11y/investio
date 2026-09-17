const WORDPRESS_API_URL =
  process.env.WORDPRESS_API_URL || "http://localhost:8081/wp-json/wp/v2";

export type BlogPost = {
  id: number;
  slug: string;
  date: string;
  title: { rendered: string };
  excerpt: { rendered: string };
  content: { rendered: string };
  _embedded?: {
    "wp:featuredmedia"?: Array<{ source_url: string }>;
    author?: Array<{ name: string }>;
  };
};

export async function getBlogPosts(
  page = 1,
  perPage = 9
): Promise<BlogPost[]> {
  try {
    const res = await fetch(
      `${WORDPRESS_API_URL}/posts?_embed&page=${page}&per_page=${perPage}`,
      { cache: "no-store" }
    );
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export async function getBlogPostBySlug(slug: string): Promise<BlogPost | null> {
  try {
    const res = await fetch(
      `${WORDPRESS_API_URL}/posts?slug=${encodeURIComponent(slug)}&_embed`,
      { cache: "no-store" }
    );
    if (!res.ok) return null;
    const posts: BlogPost[] = await res.json();
    return posts[0] ?? null;
  } catch {
    return null;
  }
}

export function getFeaturedImageUrl(post: BlogPost): string | null {
  return post._embedded?.["wp:featuredmedia"]?.[0]?.source_url ?? null;
}

export function getAuthorName(post: BlogPost): string | null {
  return post._embedded?.author?.[0]?.name ?? null;
}

export function stripHtml(html: string): string {
  return html.replace(/<[^>]*>/g, "").trim();
}
