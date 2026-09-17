"use client";

import { useState } from "react";
import type { ProjectImage } from "@/lib/api";

export function ProjectGallery({ images, altText }: { images: ProjectImage[]; altText: string }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const validImages = images.filter((img) => img.url);
  if (validImages.length === 0) return null;

  function showPrev() {
    setActiveIndex((prev) => {
      if (prev === null) return null;
      return (prev - 1 + validImages.length) % validImages.length;
    });
  }

  function showNext() {
    setActiveIndex((prev) => {
      if (prev === null) return null;
      return (prev + 1) % validImages.length;
    });
  }

  return (
    <>
      <section className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {validImages.map((image, index) => (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            key={image.id}
            src={image.url as string}
            alt={altText}
            onClick={() => setActiveIndex(index)}
            className="h-40 w-full cursor-pointer rounded-md object-cover transition hover:opacity-90"
          />
        ))}
      </section>

      {activeIndex !== null && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
          onClick={() => setActiveIndex(null)}
        >
          <button
            onClick={(e) => {
              e.stopPropagation();
              setActiveIndex(null);
            }}
            className="absolute top-4 right-4 text-3xl text-white hover:text-gray-300"
            aria-label="Zamknij"
          >
            &times;
          </button>

          {validImages.length > 1 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                showPrev();
              }}
              className="absolute left-4 text-4xl text-white hover:text-gray-300"
              aria-label="Poprzednie zdjecie"
            >
              &#8249;
            </button>
          )}

          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={validImages[activeIndex].url as string}
            alt={altText}
            onClick={(e) => e.stopPropagation()}
            className="max-h-[90vh] max-w-[90vw] rounded-md object-contain"
          />

          {validImages.length > 1 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                showNext();
              }}
              className="absolute right-4 text-4xl text-white hover:text-gray-300"
              aria-label="Nastepne zdjecie"
            >
              &#8250;
            </button>
          )}
        </div>
      )}
    </>
  );
}
