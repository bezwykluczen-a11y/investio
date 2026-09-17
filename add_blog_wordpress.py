#!/usr/bin/env python3
"""
Dodaje modul bloga (WordPress headless + strony /blog w Next.js) do
istniejacego projektu mvp-portal-projektow.

Uzycie: uruchom ten skrypt WEWNATRZ folderu mvp-portal-projektow
(tam gdzie jest docker-compose.yml):

    cd mvp-portal-projektow
    python3 add_blog_wordpress.py

Skrypt:
  1. Zastapi docker-compose.yml wersja z dodanymi serwisami
     wordpress + wordpress-db (zachowuje Twoje wczesniejsze poprawki:
     port 3001 dla web, NEXT_PUBLIC_API_URL=http://api:8000/api/v1).
  2. Doda frontend/src/lib/wordpress.ts (fetch do WP REST API).
  3. Doda frontend/src/app/blog/page.tsx (lista wpisow).
  4. Doda frontend/src/app/blog/[slug]/page.tsx (pojedynczy wpis).
  5. Zaktualizuje frontend/src/app/layout.tsx (link "Blog" w nawigacji).

Po uruchomieniu skryptu:
    docker compose up -d --build
    # poczekaj kilkanascie sekund, wordpress i baza musza wystartowac
    # otworz http://localhost:8081 i przejdz przez instalator WP
    # w wp-admin: Ustawienia -> Bezposrednie odnosniki -> "Nazwa wpisu" -> Zapisz
    # napisz i opublikuj testowy wpis
    # otworz http://localhost:3001/blog
"""
import os

FILES: dict[str, str] = {}

FILES["docker-compose.yml"] = '''services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: portal
      POSTGRES_PASSWORD: portal
      POSTGRES_DB: portal
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U portal"]
      interval: 5s
      timeout: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"

  minio:
    image: minio/minio:latest
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  api:
    build:
      context: .
      dockerfile: infra/docker/Dockerfile.backend
    restart: unless-stopped
    env_file:
      - backend/.env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app

  worker:
    build:
      context: .
      dockerfile: infra/docker/Dockerfile.backend
    restart: unless-stopped
    command: celery -A app.worker worker --loglevel=info
    env_file:
      - backend/.env
    depends_on:
      - redis
      - db
    volumes:
      - ./backend:/app

  web:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    restart: unless-stopped
    environment:
      NEXT_PUBLIC_API_URL: http://api:8000/api/v1
      WORDPRESS_API_URL: http://wordpress:80/wp-json/wp/v2
    ports:
      - "3001:3000"
    depends_on:
      - api
      - wordpress
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next

  wordpress-db:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: wordpress_root
    volumes:
      - wordpress_db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    restart: unless-stopped
    environment:
      WORDPRESS_DB_HOST: wordpress-db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    ports:
      - "8081:80"
    depends_on:
      - wordpress-db
    volumes:
      - wordpress_data:/var/www/html

volumes:
  db_data:
  minio_data:
  wordpress_data:
  wordpress_db_data:
'''

FILES["frontend/src/lib/wordpress.ts"] = '''const WORDPRESS_API_URL =
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
'''

FILES["frontend/src/app/blog/page.tsx"] = '''import Link from "next/link";
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
'''

FILES["frontend/src/app/blog/[slug]/page.tsx"] = '''import { notFound } from "next/navigation";
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
'''

FILES["frontend/src/app/layout.tsx"] = '''import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Portal Projektow",
  description: "Katalog i weryfikacja projektow inwestycyjnych",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pl">
      <body className="bg-gray-50 text-gray-900">
        <header className="border-b bg-white">
          <div className="mx-auto max-w-6xl px-4 py-4 flex items-center justify-between">
            <a href="/" className="font-semibold text-lg">Portal Projektow</a>
            <nav className="flex gap-4 text-sm">
              <a href="/projekty">Projekty</a>
              <a href="/blog">Blog</a>
              <a href="/jak-to-dziala">Jak to dziala</a>
              <a href="/ryzyka">Ryzyka</a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="border-t mt-16 py-6 text-center text-sm text-gray-500">
          Ta platforma nie przyjmuje platnosci, wplat ani inwestycji. Deklaracje zainteresowania
          nie sa zobowiazaniem finansowym.
        </footer>
      </body>
    </html>
  );
}
'''


def main() -> None:
    if not os.path.exists("docker-compose.yml"):
        print("UWAGA: nie widze docker-compose.yml w tym katalogu.")
        print("Upewnij sie, ze uruchamiasz skrypt wewnatrz folderu mvp-portal-projektow.")
        return

    created = 0
    for rel_path, content in FILES.items():
        os.makedirs(os.path.dirname(rel_path) or ".", exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"  napisano: {rel_path}")

    print(f"\\nZaktualizowano/dodano {created} plikow.")
    print("\\nNastepne kroki:")
    print("  docker compose up -d --build")
    print("  (poczekaj ~15-30s, wordpress + mysql musza wystartowac)")
    print("  otworz http://localhost:8081 i przejdz przez instalator WordPress")
    print("  w wp-admin: Ustawienia -> Bezposrednie odnosniki -> Nazwa wpisu -> Zapisz")
    print("  napisz i opublikuj testowy wpis")
    print("  otworz http://localhost:3001/blog")


if __name__ == "__main__":
    main()
