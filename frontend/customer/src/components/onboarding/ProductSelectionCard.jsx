import { CheckIcon } from "lucide-react";

import PillArrow from "@/components/home/PillArrow";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

/**
 * ProductSelectionCard Component
 *
 * Interactive selectable card for choosing a Sellince product:
 * - Hidden radio input paired with full-card label for keyboard/mouse accessibility.
 * - Product illustration, number badge, title, and descriptive text.
 * - Primary or secondary CTA button with PillArrow indicator.
 */
function ProductSelectionCard({
  productId,
  productNumber,
  productName,
  productDescription,
  actionLabel,
  illustrationSource,
  illustrationAlt,
  isSelected,
  isAvailable,
  onProductSelect,
  onProductAction,
}) {
  function handleProductSelectionChange() {
    onProductSelect(productId);
  }

  function handleProductAction() {
    onProductAction(productId);
  }

  return (
    <article
      className={cn(
        "bg-surface focus-within:ring-ring/40 flex h-full min-w-0 flex-col overflow-hidden rounded-xl border transition-colors focus-within:ring-3",
        isSelected ? "border-primary" : "border-border",
      )}
    >
      <input
        id={`product-${productId}`}
        name="sellince-product"
        type="radio"
        value={productId}
        checked={isSelected}
        className="peer sr-only"
        aria-label={productName}
        onChange={handleProductSelectionChange}
      />

      <label htmlFor={`product-${productId}`} className="flex flex-1 cursor-pointer flex-col">
        <span className="bg-inverse relative block h-45 overflow-hidden sm:h-48 md:h-44 lg:h-50 xl:h-54">
          <img
            src={illustrationSource}
            alt={illustrationAlt}
            className="size-full object-contain"
          />
          {isSelected ? (
            <span
              className="bg-primary text-primary-foreground absolute top-3 right-3 flex size-8 items-center justify-center rounded-full"
              aria-hidden="true"
            >
              <CheckIcon className="size-4" />
            </span>
          ) : null}
        </span>

        <span className="flex flex-1 flex-col px-6 pt-5">
          <span className="text-primary tracking-label text-xs font-semibold">
            PRODUCT {productNumber}
          </span>
          <span className="text-foreground mt-2 text-xl font-semibold sm:text-2xl">
            {productName}
          </span>
          <span className="text-muted-foreground mt-1.5 max-w-md text-sm leading-relaxed sm:text-base">
            {productDescription}
          </span>
        </span>
      </label>

      <div className="px-6 pt-4 pb-5">
        <Button
          type="button"
          variant={isAvailable ? "default" : "secondary"}
          className="h-12 w-full rounded-full pr-1.5 pl-5 text-sm sm:w-auto sm:text-base"
          onClick={handleProductAction}
        >
          {actionLabel}
          <PillArrow
            className={cn("ml-2", isAvailable ? undefined : "bg-inverse text-inverse-foreground")}
          />
        </Button>
      </div>
    </article>
  );
}

export default ProductSelectionCard;
